import argparse
import logging
from .main import process_files

logging.basicConfig(level=logging.INFO)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a Jinja2 template using GeoJSON data."
    )
    parser.add_argument("input", help="Path to the GeoJSON file or folder")
    parser.add_argument("template", help="Path to the Jinja2 template file")
    parser.add_argument(
        "--output",
        help="Path to save the output GeoJSON file, otherwise stdout",
    )
    args = parser.parse_args()

    process_files(args.input, args.template, args.output)


if __name__ == "__main__":
    main()
