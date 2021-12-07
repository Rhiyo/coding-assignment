import pytest
import json
import random
from coding_assignment.fwf_parser import FwfParser


@pytest.fixture
def fwf_parser():
    fwf_parser = FwfParser()
    fwf_parser.spec = {
        "ColumnNames": [
            "code1",
            "code2",
        ],
        "Offsets": ["8", "12"],
        "FixedWidthEncoding": "windows-1252",
        "IncludeHeader": "True",
        "DelimitedEncoding": "utf-8",
    }
    return fwf_parser


def test_set_spec(fwf_parser, tmp_path):
    spec_other = {
        "ColumnNames": [
            "code12",
            "code22",
        ],
        "Offsets": ["3", "3"],
        "FixedWidthEncoding": "windows-1252",
        "IncludeHeader": "True",
        "DelimitedEncoding": "utf-8",
    }

    p = tmp_path / "spec.json"

    with open(p, "w") as f:
        json.dump(spec_other, f)

    fwf_parser.set_spec(p)

    assert fwf_parser.spec == spec_other


def test_generate_fwf(fwf_parser, tmp_path):

    # Build test file as string
    test_rand_fwf = "code1   code2       \n"
    test_rand_fwf += "JEZ     F           \n"
    test_rand_fwf += "GZKQ4U  PD4DV20     \n"

    p = tmp_path / "random.txt"

    random.seed(555)
    fwf_parser.generate_fwf(p, 2)
    with open(p, "r") as f:
        rand_fwf = f.read()

    assert test_rand_fwf == rand_fwf


def test_to_csv(fwf_parser, tmp_path):

    # Build test file as string
    test_rand_csv = "code1,code2\n"
    test_rand_csv += "JEZ,F\n"
    test_rand_csv += "GZKQ4U,PD4DV20\n"

    p_csv = tmp_path / "random.txt"
    p_to = tmp_path / "random.csv"

    random.seed(555)
    fwf_parser.generate_fwf(p_csv, 2)
    fwf_parser.to_csv(p_csv, p_to)

    with open(p_to, "r") as f:
        rand_csv = f.read()
    assert test_rand_csv == rand_csv
