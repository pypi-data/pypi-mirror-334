import json
import io
from pathlib import Path
import pytest

from af3cli import InputFile
from af3cli.io import read_json, write_json


@pytest.fixture(scope="module")
def sample_data() -> str:
    return """{\n
        \"name": \"test\",\n
        \"version\": 1,\n
        \"dialect\": \"alphafold3\",\n
        \"modelSeeds\": [1, 2],\n
        \"sequences\": [\n
            {\n
                \"protein\": {\n
                    \"id\": \"A\",\n
                    \"sequence\": "MVKVGVNGFGRIGRL\"\n
                },\n
                \"protein\": {\n
                    \"id\": \"B\",\n
                    \"sequence\": "MVKVGVNGFGRIGRL\",\n
                    \"templates\": [\n
                        {\n
                         \"mmcif": \"test\",
                         \"queryIndices\": [0, 1, 2, 4, 5, 6],\n
                         \"templateIndices\": [0, 1, 2, 3, 4, 8]\n
                        }\n
                    ]\n
                },\n
                \"protein\": {\n
                    \"id\": \"C\",\n
                    \"sequence\": "MVKVGVNGFGRIGRL\"\n
                },\n
                \"rna\": {\n
                    \"id\": [\"D\"],\n
                    \"sequence\": \"AUGGUCUU\"\n
                },\n
                \"rna\": {\n
                    \"id\": [\"E\"],\n
                    \"sequence\": \"AUGGUCUU\",\n
                    \"unpairedMsa\": \"A3M\",\n
                    \"templates\": []\n
                },\n
                \"dna\": {\n
                    \"id\": [\"F\"],\n
                    \"sequence\": \"GACCTCT\",\n
                    \"modifications\": [\n
                        {\"modificationType\": \"6OG\", \"basePosition\": 1},\n
                        {\"modificationType\": \"6MA\", \"basePosition\": 2}\n
                    ]\n
                },\n
                \"ligand\": {\n
                    \"id": \"G\",\n
                    \"smiles\": \"CCC\"\n
                },\n
                \"ligand\": {\n
                    \"id": \"H\",\n
                    \"ccdCodes\": [\"NAG\", \"FUC\"]\n
                }\n\n
            }\n
        ]\n
    }"""


@pytest.fixture(scope="module")
def sample_data_dict(sample_data: str) -> dict:
    content = io.StringIO(sample_data)
    return json.load(content)


@pytest.fixture
def tmp_file_read(tmp_path: Path, sample_data_dict: dict) -> Path:
    tmp_file = tmp_path / "test_read.json"
    with open(tmp_file, "w") as json_file:
        json.dump(sample_data_dict, json_file, indent=4)
    return tmp_file


def test_json_reader(tmp_file_read: Path, sample_data_dict: dict) -> None:
    afinput = read_json(str(tmp_file_read.resolve()))
    assert afinput.name == sample_data_dict["name"]
    assert afinput.version == sample_data_dict["version"]
    assert afinput.dialect == sample_data_dict["dialect"]
    assert sorted(list(afinput.seeds)) == sorted(sample_data_dict["modelSeeds"])
    assert len(afinput.sequences) == len(sample_data_dict["sequences"])


@pytest.fixture
def tmp_file_write(tmp_path: Path) -> Path:
    return tmp_path / "test_write.json"


def test_json_rw(
        tmp_file_write: Path,
        tmp_file_read: Path,
        sample_data_dict: dict
) -> None:
    afinput = InputFile.read(str(tmp_file_read.resolve()))
    afinput.write(str(tmp_file_write))
    assert tmp_file_write.exists()

    afinput = InputFile.read(str(tmp_file_write.resolve()))
    assert afinput.name == sample_data_dict["name"]
    assert afinput.version == sample_data_dict["version"]
    assert afinput.dialect == sample_data_dict["dialect"]
    assert sorted(list(afinput.seeds)) == sorted(sample_data_dict["modelSeeds"])
    assert len(afinput.sequences) == len(sample_data_dict["sequences"])
