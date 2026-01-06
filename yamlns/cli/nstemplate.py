#!/usr/bin/python3

from ..nstemplate import apply, extract
import sys


def main(args=sys.argv):  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(
        description="Takes a template and extract a yaml to fill it.",
    )
    parser.add_argument(
        "--encoding",
        default=None,
        help="forces input encoder for templates",
        dest="encoding",
    )

    sub = parser.add_subparsers(
        dest="subcommand",
    )

    subparser = sub.add_parser(
        "extract",
        help="Collects the template vars from a template and renders an empty yaml file with them",
    )
    subparser.add_argument(
        metavar="input.template",
        dest="input_template",
    )
    subparser.add_argument(
        metavar="output.yaml",
        dest="output_yaml",
    )

    subparser = sub.add_parser(
        "apply",
        help="Apply structured data in a YAML file to a template",
    )
    subparser.add_argument(
        metavar="input.yaml",
        dest="input_yaml",
    )
    subparser.add_argument(
        metavar="template",
        dest="template",
    )
    subparser.add_argument(
        metavar="output",
        dest="output",
    )

    args = parser.parse_args()

    if args.subcommand == "extract":
        extract(args.input_template, args.output_yaml, args.encoding)
        return 0

    if args.subcommand == "apply":
        apply(args.input_yaml, args.template, args.output, args.encoding)
        return 0

    parser.print_help()
    return -1


def deprecated():  # pragma: no cover
    print(
        "The script nstemplate.py is deprecated. "
        "Use nstemplate instead (without the .py extension)"
    )
    sys.exit(-1)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


# vim: sw=4 ts=4 noet
