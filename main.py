import argparse
import options

import image_converter


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
        choices=list(options.MediaType),
        default=options.MediaType.STATIC,
    )
    # parser.add_argument()

    args = parser.parse_args()

    image_converter.image_to_ascii(args.path)


if __name__ == "__main__":
    main()
