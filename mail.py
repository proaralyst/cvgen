#!/usr/bin/env python3

# Standard imports
import argparse
import sys

# Non-standard imports
import jinja2

def main(args):
    parser = argparse.ArgumentParser(description="Builds a CV using a YAML database.")

    args = parser.parse_args(args)

if __name__ == "__main__":
    main(sys.argv[1:])
