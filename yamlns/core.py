import yaml
from collections import OrderedDict
from .compat import Path, text

_sorted = sorted


class namespace(OrderedDict):
    """
    A dictionary whose values can be accessed also as attributes
    and can be loaded and dumped as YAML.
    """

    def __init__(self, *args, **kwd):
        super(namespace, self).__init__(*args, **kwd)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super(namespace, self).__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            super(namespace, self).__delattr__(name)

    def __getitem__(self, name):
        if not hasattr(name, "split"):
            return super(namespace, self).__getitem__(name)
        parts = name.split(".", 1)
        result = super(namespace, self).__getitem__(parts[0])
        if parts[1:]:
            return result[parts[1]]
        return result

    def __setitem__(self, name, value):
        if not hasattr(name, "split"):
            return super(namespace, self).__setitem__(name, value)
        parts = name.split(".", 1)
        if not parts[1:]:
            return super(namespace, self).__setitem__(parts[0], value)
        level = self.setdefault(parts[0], ns())
        level[parts[1]] = value

    def __dir__(self):

        def isidentifier(candidate):
            "Is the candidate string an identifier in Python 2.x"
            try:
                return candidate.isidentifier()
            except AttributeError:
                pass
            import keyword
            import re

            is_not_keyword = candidate not in keyword.kwlist
            pattern = re.compile(r"^[a-z_][a-z0-9_]*$", re.I)
            matches_pattern = bool(pattern.match(candidate))
            return is_not_keyword and matches_pattern

        try:
            attributes = super(namespace, self).__dir__()
        except AttributeError:  # Py2 OrderedDict has no __dir__
            attributes = []
        attributes.extend(k for k in self.keys() if isidentifier(k))
        return attributes

    def deepcopy(self):
        return self.loads(self.dump())

    @classmethod
    def deep(cls, x, sorted=False):
        """Turns recursively all the dicts of a json like
        structure into yamlns namespaces. Set sorted to true
        to force alphabetical order of the keys
        so that their dumps can be compared.
        """
        sort_function = _sorted if sorted else lambda x: x
        if type(x) in (dict, namespace):
            return ns(
                (k, cls.deep(v, sorted=sorted)) for k, v in sort_function(x.items())
            )
        if type(x) in (list, tuple):
            return [cls.deep(y, sorted=sorted) for y in x]
        return x

    @classmethod
    def loads(cls, yamlContent):
        yamlContent = text(yamlContent)
        import io

        return cls.load(io.StringIO(yamlContent))

    @classmethod
    def load(cls, source):
        from .serialization import NamespaceYAMLLoader

        # Already open read file
        if hasattr(source, "read"):
            return yaml.load(stream=source, Loader=NamespaceYAMLLoader)

        with Path(source).open() as f:
            return yaml.load(stream=f, Loader=NamespaceYAMLLoader)

    def dump(self, target=None):

        def dumpit(stream):
            from .serialization import NamespaceYamlDumper

            return yaml.dump(
                self,
                stream=stream,
                default_flow_style=False,
                allow_unicode=True,
                Dumper=NamespaceYamlDumper,
            )

        if target is None:
            return dumpit(target)

        # Already open write file
        if hasattr(target, "write"):
            return dumpit(target)

        import sys

        mode = "wb" if sys.version_info[0] == 2 else "w"

        with Path(target).open(mode) as f:
            return dumpit(f)

    @classmethod
    def fromTemplateVars(clss, templateContent):
        """Given a string with format template substitutions
        it builds a namespace having the fields to fill it.
        Namespace leaf values will be set as empty strings.
        """
        templateVariables = _collectVars(templateContent)
        return _varsTree(templateVariables)


def _collectVars(content):
    import re

    pattern = r"{([^}^[]*)(\[[^]]\])?}"
    return [item.group(1) for item in re.finditer(pattern, content)]


def _varsTree(theVars):
    ns = namespace()
    for segments in (var.split(".") for var in sorted(theVars)):
        target = ns
        for segment in segments[:-1]:
            if segment not in target:
                target[segment] = namespace()
            # TODO: double check it is a ns
            target = target[segment]
        target[segments[-1]] = ""
    return ns


ns = namespace  # alias

# vim: sw=4 ts=4 noet
