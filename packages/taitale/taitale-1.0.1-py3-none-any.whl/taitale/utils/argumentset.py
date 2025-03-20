from dataclasses import dataclass, field


@dataclass
class ArgumentSet:
    args: dict = field(default_factory=dict)

    def get(self, key):
        return self.args[key]

    def set(self, key: str, value: str):
        self.args[key] = value

    def update(self, **kwargs):
        self.args.update(kwargs)

    def merge(self, other: "ArgumentSet"):
        self.args = {**self.args, **other.args}
