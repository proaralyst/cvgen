#!/usr/bin/env python3

# Standard imports
import argparse
import sys
import os.path

# Non-standard imports
import jinja2
import yaml

def filter_db(db, tags):
    return db

def main(args):
    parser = argparse.ArgumentParser(description="Builds a CV using a YAML database.")
    parser.add_argument("source", help="The YAML database to source from.")
    parser.add_argument("template", help="The template to build the CV from.")
    parser.add_argument("output", help="The file to output.")
    parser.add_argument("--tags", help="A comma-separated list of tags. If present, only items tagged with those specified appear in the output.")

    args = parser.parse_args(args)

    tags = None
    if args.tags is not None:
        tags = args.tags.split(",")

    db = None
    with open(args.source, "r") as source_file:
        db = yaml.load(source_file)

    if tags is not None:
        db = filter_db(db, tags)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(args.template)))
    template = None
    try:
        template = env.get_template(os.path.basename(args.template))
    except jinja2.TemplateSyntaxError as ex:
        print(
            ("Failed to load template from {filename}. "
            "Error on line {lineno}: {message}").format(
                filename=ex.filename,
                lineno=ex.lineno,
                message=ex.message))
        sys.exit(1)

    with open(args.output, "w") as output_file:
        output_file.write(template.render(db))

if __name__ == "__main__":
    main(sys.argv[1:])
