import configparser
from dataclasses import dataclass, field
from typing import Optional, Union

from .argumentset import ArgumentSet


# The concept of a group is to improve DX
@dataclass
class Parset(ArgumentSet):
    # @parameter prefix Defines the prefix of the Parset eg Csimulator, Cimager
    # @parameter group Defines the group values belong to
    prefix: Optional[str] = None
    group_name: Optional[str] = None
    prefix_ser: str = field(init=False)

    def __post_init__(self):
        super().__init__()
        self.prefix_ser = f"{self.prefix}." if self.prefix else ""

    # TODO: Find a better name for this
    def value(self, value):
        self.set(f"{self.prefix}", value)

    def comment(self, comment: str):
        # The simplest way to serialize define this, definetly can be improved
        comment = f"# {comment}"
        self.set(comment, comment)

    def merge(self, other: Union[ArgumentSet, "Parset"], dropPrefix=False):
        """Merge another ArgumentSet or Parset into this one.

        Args:
            other: The ArgumentSet or Parset to merge from
            dropPrefix: Only used when merging from another Parset. If True, drops the prefix when merging.
        """
        if isinstance(other, ArgumentSet) and not isinstance(other, Parset):
            # Simple merge for ArgumentSet
            for k, v in other.args.items():
                self.set(k, v)
        else:
            # Merge from another Parset
            if dropPrefix:
                for k, v in other.args.items():
                    if self.prefix and k.startswith(f"{self.prefix_ser}"):
                        self.args[k[len(self.prefix_ser) :]] = v
                    else:
                        self.args[k] = v
            else:
                # Add prefix when merging from another Parset
                for k, v in other.args.items():
                    if not k.startswith("#"):
                        if other.prefix and k == other.prefix:
                            self.set(f"{k}", v)
                        else:
                            self.set(f"{other.prefix}.{k}", v)
                    else:
                        self.comment(v)

    def _deser(self, content):
        config = configparser.ConfigParser(interpolation=None)
        # Preserve case sensitivity
        config.optionxform = str
        # Add a section as there is no section in the file
        content = f"[DEFAULT]\n{content}"
        config.read_string(content)

        result = Parset(prefix=self.prefix)
        for key, v in config["DEFAULT"].items():
            if v == "true":
                v = True
            elif v == "false":
                v = False
            result.set(key, v)
        return result

    def parse_string(self, content):
        defaults = self._deser(content)
        self.merge(defaults, dropPrefix=True)

    def group(self, *group_keys):
        prefix = ".".join(group_keys)

        def group_set(key, value):
            self.set(f"{prefix}.{key}", value)

        return group_set

    def read_from_file(self, filename: str):
        """Read parset configuration from a file

        Args:
            filename: Path to the parset configuration file
        """
        with open(filename) as stream:
            # Add a section as there is no section in the file
            content = stream.read()
            defaults = self._deser(content)
            self.merge(defaults, dropPrefix=True)

    def get(self, key):
        """Get a value by key. If the key is not found and we have a prefix, try with the prefix."""
        try:
            return self.args[key]
        except KeyError:
            if self.prefix:
                prefixed_key = f"{self.prefix_ser}{key}"
                return self.args[prefixed_key]
            raise

    def to_string(self):
        content = []
        for k, v in self.args.items():
            if k == self.prefix:
                content.append(f"{k} = {v}")
            elif not k.startswith("#"):
                if isinstance(v, bool):
                    v = "true" if v is True else "false"
                # print(self.prefix_ser, k, v)
                content.append(f"{self.prefix_ser}{k} = {v}")
            else:
                content.append(k)

        return "\n".join(content) + "\n"

    def serialize(self, filename):
        with open(filename, "w+") as stream:
            stream.write(self.to_string())
            stream.close()
