import pytest
import random

from af3cli.builder import InputBuilder
from af3cli.input import InputFile
from af3cli.bond import Atom, Bond
from af3cli.ligand import Ligand, LigandType, CCDLigand, SMILigand
from af3cli.sequence import Sequence, SequenceType


@pytest.fixture(scope="module")
def builder() -> InputBuilder:
    return InputBuilder()


@pytest.fixture(scope="module")
def sample_sequence() -> Sequence:
    return Sequence(
        seq_type=SequenceType.PROTEIN,
        seq_str="MVKVGVNGFGRIGRLVTRAAFNS",
        seq_id=["A", "B"]
    )


@pytest.fixture(scope="module")
def sample_ligand() -> Ligand:
    return Ligand(
        ligand_type=LigandType.CCD,
        ligand_value=["NAC"],
        seq_id=["C", "D"]
    )

@pytest.fixture(scope="module")
def sample_ccdligand() -> CCDLigand:
    return CCDLigand(
        ligand_value=["NAC"],
        seq_id=["E"]
    )

@pytest.fixture(scope="module")
def sample_smiligand() -> SMILigand:
    return SMILigand(
        ligand_value="CCOCC",
        seq_id=["F"]
    )

@pytest.fixture(scope="module")
def sample_bond() -> Bond:
    atom1 = Atom.from_string("A:1:CA")
    atom2 = Atom.from_string("B:1:CA")
    return Bond(atom1, atom2)


def test_builder_set_name(builder: InputBuilder) -> None:
    builder.set_name("test")
    assert builder.build().name == "test"


@pytest.mark.parametrize("seeds", [
    [1, 2], [1, 2, 3], [random.randint(1, 100) for _ in range(5)]
])
def test_builder_set_seeds(builder: InputBuilder, seeds: list[int]) -> None:
    builder.set_seeds(seeds)
    assert sorted(list(builder.build().seeds)) == sorted(list(set(seeds)))


def test_builder_set_version(builder: InputBuilder) -> None:
    builder.set_version(1)
    assert builder.build().version == 1


def test_builder_set_dialect(builder: InputBuilder) -> None:
    builder.set_dialect("alphafold3")
    assert builder.build().dialect == "alphafold3"


def test_builder_add_sequence(
        builder: InputBuilder,
        sample_sequence: Sequence
) -> None:
    builder.add_sequence(sample_sequence)
    input_file = builder.build()
    input_seq = input_file.sequences[0]
    assert input_seq.sequence == sample_sequence.sequence
    assert input_seq.sequence_type == sample_sequence.sequence_type


def test_builder_add_ligand(
        builder: InputBuilder,
        sample_ligand: Ligand,
        sample_ccdligand: CCDLigand,
        sample_smiligand: SMILigand
) -> None:
    for i, lig in enumerate([sample_ligand, sample_ccdligand, sample_smiligand]):
        builder.add_ligand(lig)
        input_file = builder.build()
        assert input_file.ligands[-1].ligand_value == lig.ligand_value
        assert input_file.ligands[-1].ligand_type == lig.ligand_type


def test_builder_add_bond(builder: InputBuilder, sample_bond: Bond) -> None:
    builder.add_bonded_atom_pair(sample_bond)
    input_file = builder.build()
    assert input_file.bonded_atoms[0].atom1.eid == sample_bond.atom1.eid
    assert input_file.bonded_atoms[0].atom1.resid == sample_bond.atom1.resid
    assert input_file.bonded_atoms[0].atom1.name == sample_bond.atom1.name
    assert input_file.bonded_atoms[0].atom2.eid == sample_bond.atom2.eid
    assert input_file.bonded_atoms[0].atom2.resid == sample_bond.atom2.resid
    assert input_file.bonded_atoms[0].atom2.name == sample_bond.atom2.name


def test_builder_user_ccd(builder: InputBuilder) -> None:
    builder.set_user_ccd("ccdString")
    assert builder.build().user_ccd == "ccdString"


def test_builder_build(builder: InputBuilder) -> None:
    afinput = builder.build()
    assert isinstance(afinput, InputFile)
    assert afinput.seeds is not None
    assert len(afinput.sequences) > 0
    assert len(afinput.ligands) > 0
    assert len(afinput.bonded_atoms) > 0


def test_builder_attach(builder: InputBuilder) -> None:
    curr_input = builder.build()
    builder.attach(curr_input)
    assert builder.build() == curr_input


def test_builder_reset_ids(
        builder: InputBuilder,
        sample_sequence: Sequence
) -> None:
    curr_input = builder.build()

    for seq_type in [curr_input.sequences, curr_input.ligands]:
        for entry in seq_type:
            assert entry.get_id() is not None

    builder.reset_ids()

    for seq_type in [curr_input.sequences, curr_input.ligands]:
        for entry in seq_type:
            assert entry.get_id() is None
