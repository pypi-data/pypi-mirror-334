#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

import grpc
import soundfile
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict, Parse, ParseError
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
)
from phonexia.grpc.technologies.keyword_spotting.v1.keyword_spotting_pb2 import (
    DetectRequest,
    DetectResponse,
    Keyword,
    ListAllowedSymbolsRequest,
    ListAllowedSymbolsResponse,
)
from phonexia.grpc.technologies.keyword_spotting.v1.keyword_spotting_pb2_grpc import (
    KeywordSpottingStub,
)


def print_json(message, output_file: Optional[Path] = None) -> None:
    json.dump(
        message, output_file.open("w") if output_file else sys.stdout, indent=2, ensure_ascii=False
    )


def message_to_dict(message):
    return MessageToDict(
        message,
        always_print_fields_with_no_presence=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
    )


def time_to_duration(time: float) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: str,
    keywords: list[Keyword],
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
) -> Iterator[DetectRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield DetectRequest(
                    audio=Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    keywords=keywords,
                )
                time_range = None
                raw_audio_config = None
                keywords = None

    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(chunk_size):
                yield DetectRequest(
                    audio=Audio(content=chunk, time_range=time_range),
                    keywords=keywords,
                )
                time_range = None
                keywords = None


def write_result(response: DetectResponse, output_file: Optional[str] = None) -> None:
    logging.debug("Writing matches to {}".format(output_file if output_file else "'stdout'"))
    message = message_to_dict(message=response)
    print_json(message, output_file)


def detect_keywords(
    channel: grpc.Channel,
    keyword_list: Path,
    input_file: Path,
    output_file: Optional[Path],
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
) -> None:
    logging.info(
        "Detecting keywords from {input} -> {output}".format(
            input=input_file, output=(output_file if output_file else "'stdout'")
        )
    )
    with open(keyword_list) as f:
        parsed_keyword_list = Parse(text=f.read(), message=DetectRequest())
        keywords = parsed_keyword_list.keywords

    response_it = make_request(
        file=input_file,
        keywords=keywords,
        start=start,
        end=end,
        use_raw_audio=use_raw_audio,
    )

    stub = KeywordSpottingStub(channel)
    for response in stub.Detect(response_it, metadata=metadata):
        write_result(response, output_file)


def list_allowed_symbols(
    channel: grpc.Channel, output_file: Optional[Path], metadata: Optional[list]
):
    logging.info("Listing allowed symbols")
    stub = KeywordSpottingStub(channel)

    logging.debug("Writing symbols to {}".format(output_file if output_file else "'stdout'"))
    response: ListAllowedSymbolsResponse = stub.ListAllowedSymbols(
        ListAllowedSymbolsRequest(), metadata=metadata
    )

    message = message_to_dict(message=response)
    print_json(message, output_file)


# Main program
def handle_grpc_error(e: grpc.RpcError):
    logging.error(f"gRPC call failed with status code: {e.code()}")
    logging.error(f"Error details: {e.details()}")

    if e.code() == grpc.StatusCode.UNAVAILABLE:
        logging.error("Service is unavailable. Please try again later.")
    elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        logging.error("Invalid arguments were provided to the RPC.")
    elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        logging.error("The RPC deadline was exceeded.")
    else:
        logging.error(f"An unexpected error occurred: {e.code()} - {e.details()}")


def check_file_exists(path: Path) -> Path:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist.")
    return Path(path)


def main():
    parser = argparse.ArgumentParser(
        description=("Detects keywords in an audio file"),
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=check_file_exists,
        help="Output result to a file. If omitted, output to stdout.",
    )
    parser.add_argument(
        "-k",
        "--keyword_list",
        type=check_file_exists,
        help="Path to a file containing a list of keywords. You can generate reference list by "
        "running this client with '--example_keyword_list' argument.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output result to a file. If omitted, output to stdout.",
    )
    parser.add_argument(
        "--list_allowed_symbols", action="store_true", help="List allowed graphemes and phonemes"
    )
    parser.add_argument(
        "--example_keyword_list", action="store_true", help="Generate example keyword list"
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")

    args = parser.parse_args()

    output_file: Optional[Path] = Optional
    output_file = args.output

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {args.host}")
        channel = (
            grpc.secure_channel(target=args.host, credentials=grpc.ssl_channel_credentials())
            if args.use_ssl
            else grpc.insecure_channel(target=args.host)
        )

        start_time = datetime.now()

        if args.list_allowed_symbols:
            list_allowed_symbols(
                channel=channel,
                output_file=args.output,
                metadata=args.metadata,
            )

        elif args.example_keyword_list:
            keyword_list = {
                "keywords": [
                    {
                        "spelling": "frumious",
                        "pronunciations": ["f r u m i o s", "f r u m i u s"],
                    },
                    {
                        "spelling": "flibbertigibbet",
                        "pronunciations": ["f l i b r t i j i b i t", "f l i b r t i j i b e t"],
                    },
                ]
            }
            print_json(keyword_list, output_file)

        else:
            if not args.keyword_list or not args.input:
                logging.error("Missing keyword list or input file")
                exit(1)

            detect_keywords(
                channel=channel,
                keyword_list=args.keyword_list,
                input_file=args.input,
                output_file=output_file,
                start=args.start,
                end=args.end,
                metadata=args.metadata,
                use_raw_audio=args.use_raw_audio,
            )

        logging.debug(f"Elapsed time {(datetime.now() - start_time)}")

    except grpc.RpcError as e:
        handle_grpc_error(e)
        exit(1)
    except ParseError:
        logging.exception("Error while parsing keyword list")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
