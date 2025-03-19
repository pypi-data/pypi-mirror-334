class Version(str):
    def __init__(self, version: str):
        self.version = version

    def __repr__(self):
        return f"Version(anygrad={self.version})"

    __module__ = "anygrad"


__version__ = Version("0.0.4")
