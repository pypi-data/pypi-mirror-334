import argparse
import logging
import os
import sys
from typing import Any, Dict

from .guacenc_encode import encode_recording


def setup_logging(verbosity: int) -> None:
    """
    Configure logging based on verbosity level.
    
    Args:
        verbosity (int): 0 for normal output, 1 for verbose (-v), 2 for very verbose (-vv)
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
        # First, configure the root logger to a high level to suppress other packages' logs
    logging.basicConfig(
        level=logging.WARNING,  # Default level for all loggers
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get the root logger and set its level high to suppress most logs
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.ERROR)  # Only show errors from other libraries

    # Create our application logger
    app_logger = logging.getLogger('guacenc')
    # Remove any existing handlers to avoid duplicate logs
    for handler in app_logger.handlers[:]:
        app_logger.removeHandler(handler)
    # Create console handler
    console_handler = logging.StreamHandler()
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)


    # Set the appropriate log level based on verbosity
    if verbosity == -1:  # Quiet mode
        app_logger.setLevel(logging.ERROR)
    elif verbosity == 0:  # Normal mode
        app_logger.setLevel(logging.WARNING)
    elif verbosity == 1:  # Verbose mode
        app_logger.setLevel(logging.INFO)
    else:  # verbosity >= 2, Very verbose mode
        app_logger.setLevel(logging.DEBUG)
    # Add the handler to our application logger
    app_logger.addHandler(console_handler)

    # Set propagate to False to prevent logs from propagating to the root logger
    app_logger.propagate = False



    # Control FFmpeg logs based on verbosity
    if verbosity >= 2:
        logging.getLogger('ffmpeg').setLevel(logging.INFO)
    else:
        logging.getLogger('ffmpeg').setLevel(logging.ERROR)

    # Log that logging has been set up at the appropriate level
    if verbosity >= 2:
        app_logger.debug("Debug logging enabled (very verbose mode)")
    elif verbosity == 1:
        app_logger.info("Verbose logging enabled")
    elif verbosity == -1:
        pass  # No output in quiet mode
    else:
        app_logger.warning("Normal logging mode (warnings and errors only)")



def parse_arguments() -> Dict[str, Any]:
    """
    Parse command line arguments for the guacenc encoder.
    
    Returns:
        Dict[str, Any]: Dictionary with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="guacenc-py - Guacamole recording encoder"
    )

    # Required arguments
    parser.add_argument(
        "-i","--input",
        help="Input file or directory containing the recording"
    )

    parser.add_argument(
        "-o","--output",
        help="Output file for the encoded video"
    )

    # Optional arguments
    parser.add_argument(
        "--size",
        type=str,
        default="1024x768",
        help="Output video dimensions (default: 1024x768)"
    )

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "-v", "--verbose",
        action="store_const",
        const=1,
        default=0,
        dest="verbosity",
        help="Verbose output"
    )
    verbosity_group.add_argument(
        "-vv", "--very-verbose",
        action="store_const",
        const=2,
        dest="verbosity",
        help="Very verbose output (including debug information)"
    )
    verbosity_group.add_argument(
        "-q", "--quiet",
        action="store_const",
        const=-1,
        dest="verbosity",
        help="Suppress all output except errors"
    )

    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        sys.exit(1)
    # Validate input exists
    if not os.path.exists(args.input):
        parser.error(f"Input file or directory does not exist: {args.input}")

    return vars(args)


def main() -> None:
    """
    Main entry point for the CLI.
    """
    args = parse_arguments()
    setup_logging(args["verbosity"])
    encode_recording(
        input_path=args["input"],
        output_path=args["output"],
        size=args["size"],
        verbosity=args["verbosity"]
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
