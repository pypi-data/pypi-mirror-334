from pathlib import Path
from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile
from pyconverters_mistralocr.mistralocr import MistralOCRConverter, MistralOCRParameters


@pytest.mark.skip(reason="Not a test")
def test_mistralocr_pdf():
    converter = MistralOCRConverter()
    parameters = MistralOCRParameters(segment=True)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Sodexo_URD_2023_FR - 4p.pdf")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "application/pdf"), parameters
        )
    assert len(docs) == 1
    assert docs[0].identifier == 'Sodexo_URD_2023_FR - 4p.pdf'
    assert docs[0].title == "Une performance solide au cours de l'exercice 2023 "

    json_file = source.with_suffix(".json")
    with json_file.open("w") as fout:
        print(docs[0].json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
