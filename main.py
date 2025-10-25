import argparse
import options

import image_converter
import validators


def main():
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

    args = parser.parse_args()

    validators.ArgsValidator.validate_parameters(args)

    image = image_converter.ImageConverter(
        image_path=args.path,
        colored=args.colored,
        output_path=args.output_path,
    )
    image.print_ascii_image()


if __name__ == "__main__":
    main()
