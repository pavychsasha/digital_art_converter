import argparse
import options

import utils.validators


def initialzie_argparser():
    parser = argparse.ArgumentParser(
        prog="Image to ASCII converter",
        description="This program converst jpg and image to ascii format",
    )

    parser.add_argument("-p", "--path", type=str, required=True)
    parser.add_argument(
        "-t",
        "--type",
        type=options.MediaType,
        choices=[mt.value for mt in options.MediaType],
        default=options.MediaType.STATIC,
    )
    parser.add_argument(
        "-c",
        "--colored",
        type=bool,
        default=False,
    )

    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        help="TXT file you want to store the ",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        help=(
            "Threshold of the media file, positive integer [0-255], "
            "if not specified, program automatically defines a threshold by a 92nd percentile"
        ),
    )

    parser.add_argument(
        "--output_type",
        type=options.OutputType,
        choices=[ot.value for ot in options.OutputType],
        default=options.OutputType.CONSOLE,
    )

    args = parser.parse_args()

    utils.validators.ArgsValidator.validate_parameters(args)
    return args
