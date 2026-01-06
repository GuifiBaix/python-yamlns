#!/usr/bin/python3

from .core import ns
from .compat import text, Path


def apply(yamlfile, template, output, encoding="utf-8"):
    """
    Fills a template file with data in yamlfile to generate output.
    """
    data = ns.load(yamlfile)
    content = Path(template).read_text(encoding=encoding)
    result = content.format(**data)
    Path(output).write_text(text(result, encoding=encoding), encoding=encoding)


def extract(input_template, output_yaml, encoding="utf-8"):
    """
    Extracts a yaml file with the attribute structure deduced from template value insertions
    and empty values so you can edit them and provide the proper data.
    """
    content = Path(input_template).read_text(encoding=encoding)
    schema = ns.fromTemplateVars(content)
    Path(output_yaml).write_text(
        text(schema.dump(), encoding=encoding), encoding=encoding
    )


# vim: sw=4 ts=4 noet
