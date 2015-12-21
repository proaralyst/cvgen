#!/usr/bin/env python3

# Standard imports
import argparse
import sys

# Non-standard imports
import jinja2

def main(args):
    parser = argparse.ArgumentParser(description="Builds a CV using a YAML database.")
    parser.add_argument("source", help="The YAML database to source from.")
    parser.add_argument("template", help="The template to build the CV from.")
    parser.add_argument("output", help="The file to output.")

    args = parser.parse_args(args)

if __name__ == "__main__":
    main(sys.argv[1:])
