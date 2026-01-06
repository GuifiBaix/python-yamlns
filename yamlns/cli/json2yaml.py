import sys
from ..core import ns

def main(): # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(
        description="Converts JSON into pretty printed YAML.",
    )
    args = parser.parse_args()

    data = ns.load(sys.stdin)
    data.dump(sys.stdout)



