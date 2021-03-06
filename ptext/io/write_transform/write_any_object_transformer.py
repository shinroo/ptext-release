import io
from typing import Optional, Union

from ptext.io.read_transform.types import AnyPDFType
from ptext.io.write_transform.ascii_art.write_ascii_art_transformer import (
    WriteASCIIArtTransformer,
)
from ptext.io.write_transform.image.write_image_transformer import WriteImageTransformer
from ptext.io.write_transform.object.write_array_transformer import (
    WriteArrayTransformer,
)
from ptext.io.write_transform.object.write_dictionary_transformer import (
    WriteDictionaryTransformer,
)
from ptext.io.write_transform.object.write_stream_transformer import (
    WriteStreamTransformer,
)
from ptext.io.write_transform.primitive.write_boolean_transformer import (
    WriteBooleanTransformer,
)
from ptext.io.write_transform.primitive.write_name_transformer import (
    WriteNameTransformer,
)
from ptext.io.write_transform.primitive.write_number_transformer import (
    WriteNumberTransformer,
)
from ptext.io.write_transform.primitive.write_string_transformer import (
    WriteStringTransformer,
)
from ptext.io.write_transform.reference.write_reference_transformer import (
    WriteReferenceTransform,
)
from ptext.io.write_transform.reference.write_xref_transformer import (
    WriteXREFTransformer,
)
from ptext.io.write_transform.write_base_transformer import (
    WriteTransformerContext,
    WriteBaseTransformer,
)
from ptext.io.write_transform.write_pdf_transformer import WritePDFTransformer


class WriteAnyObjectTransformer(WriteBaseTransformer):
    def __init__(self):
        super().__init__()
        # fun
        self.add_child_transformer(WriteASCIIArtTransformer())
        # special object types
        self.add_child_transformer(WritePDFTransformer())
        self.add_child_transformer(WriteXREFTransformer())
        # object types
        self.add_child_transformer(WriteArrayTransformer())
        self.add_child_transformer(WriteStreamTransformer())
        self.add_child_transformer(WriteDictionaryTransformer())
        self.add_child_transformer(WriteImageTransformer())
        # primitives
        self.add_child_transformer(WriteNameTransformer())
        self.add_child_transformer(WriteStringTransformer())
        self.add_child_transformer(WriteReferenceTransform())
        self.add_child_transformer(WriteNumberTransformer())
        self.add_child_transformer(WriteBooleanTransformer())

    def can_be_transformed(self, object_to_transform: AnyPDFType):
        return False

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
        destination: Optional[Union[io.BufferedIOBase, io.RawIOBase]] = None,
    ):
        if context is None:
            super().transform(
                object_to_transform,
                WriteTransformerContext(
                    destination=destination, root_object=object_to_transform
                ),
            )
        else:
            super().transform(object_to_transform, context)
