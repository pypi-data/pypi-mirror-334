import argparse
from dataclasses import dataclass

from .argumentset import ArgumentSet


@dataclass
class CliArgs(ArgumentSet):

    parser: argparse.ArgumentParser = None
    option_sep: str = "--"

    def set(self, key: str, value: any = True, pType="option"):
        if pType == "option":
            self.args[key] = value
        if pType == "positional":
            if "positional" in self.args and isinstance(self.args["positional"], list):
                self.args["positional"].append(key)
            else:
                self.args["positional"] = key

    def _deser(self, content):
        if self.parser is None:
            # raise ValueError("Cannot parse raw arguments without parser")
            return {"positional": content}
        args, _ = self.parser.parse_known_args(content.split(" "))
        return vars(args)

    def parse_string(self, content):
        raw_values = self._deser(content)
        self.merge(ArgumentSet(args=raw_values))

    def to_string(self):
        content = []
        # TODO: Find a better logic for this
        for k, v in self.args.items():
            if k == "positional":
                if isinstance(v, list):
                    content.append(" ".join(v))
                else:
                    content.append(v)
            elif v is True:
                content.append(f"{self.option_sep}{k}")
            elif v is False or v is None:
                pass
            else:
                if isinstance(v, list):
                    content.append(f"{self.option_sep}{k} {' '.join(v)}")
                else:
                    content.append(f"{self.option_sep}{k} {v}")
        return " ".join(content)
