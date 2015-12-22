#!/usr/bin/env python3

# Standard imports
import argparse
import sys
import os.path

# Non-standard imports
import jinja2
import yaml

class BadStructureException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def filter_dictionary(entity, tags):
    filtered = {}
    for key, subentity in entity.items():
        value = filter_db(subentity, tags)
        if value is not None:
            filtered[key] = value

    return filtered

def filter_db(entity, tags):
    """
    Performs two actions: dictionaries with a _default member have the correct tag
    selected; and any object with a tags member is omitted if its tag set produces
    an empty set on intersection with the main tag set.

    If a multi-choice element has more than one choice, the first option is
    chosen.
    """
    if type(entity) is dict:
        if "_default" in entity:
            # Find the correct tag, falling back to _default and write to filtered
            selected = False
            for tag, value in entity.items():
                if tag in tags:
                    return value
        elif "_tags" in entity:
            # Look for tags member and handle
            if type(entity["_tags"]) is not list:
                raise BadStructureException("_tags must be of type list.")

            if "_all" in entity["_tags"] or len([x for x in tags if x in entity["_tags"]]) != 0:
                return filter_dictionary(entity, tags)
            else:
                # else leave out entity
                return None
        else:
            # else leave out entity
            return None

    elif type(entity) is list:
        # Iterate over each entity and check tags
        value = []
        for item in entity:
            filtered = filter_db(item, tags)
            if filtered is not None:
                value.append(filtered)
        return value

    else:
        # Just add the entity
        return entity


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
        db["_tags"] = ["_all"]

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
