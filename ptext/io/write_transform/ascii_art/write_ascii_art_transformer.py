from pathlib import Path
from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Stream
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteASCIIArtTransformer(WriteBaseTransformer):
    def __init__(self):
        super().__init__()
        self.has_been_used = False

    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Stream) and not self.has_been_used

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Stream)

        f = Path(__file__).parent / "ascii_logo.txt"
        with open(f, "r") as logo_file_handle:
            ascii_logo = logo_file_handle.readlines()

        # append newline (if needed)
        if ascii_logo[-1][-1] != "\n":
            ascii_logo[-1] += "\n"

        # convert to latin1
        ascii_logo_bytes = [bytes("%    " + x, "latin1") for x in ascii_logo]

        self.has_been_used = True
        for x in ascii_logo_bytes:
            context.destination.write(x)
        context.destination.write(bytes("\n", "latin1"))

        self.get_root_transformer().transform(object_to_transform, context)
