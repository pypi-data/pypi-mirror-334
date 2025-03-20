import pytest

from af3cli.seqid import num_to_letters
from af3cli.seqid import IDRecord, IDRegister
from af3cli.input import InputFile
from af3cli.sequence import ProteinSequence


@pytest.mark.parametrize("num,letters", [
    (1, "A"), (2, "B"), (3, "C"), (26, "Z"),
    (27, "AA"), (28, "AB"), (52, "AZ"), (53, "BA"),
    (703, "AAA"), (704, "AAB")
])
def test_num_to_letters(num: int, letters: str) -> None:
    assert num_to_letters(num) == letters


@pytest.fixture(scope="module")
def register() -> IDRegister:
    return IDRegister()


@pytest.mark.parametrize("letter", [
    "A", "B", "C", "D"
])
def test_id_register(register: IDRegister, letter: str) -> None:
    assert register.generate() == letter


@pytest.mark.parametrize("letter", [
    "F", "G", "H", "I"
])
def test_id_register_fill(register: IDRegister, letter: str) -> None:
    register.register(letter)
    assert letter in register._registered_ids
    assert register._count == 4


@pytest.mark.parametrize("letter", [
    "E", "J", "K", "L", "M"
])
def test_id_register_filled(register: IDRegister, letter: str) -> None:
    assert register.generate() == letter


@pytest.mark.parametrize("letter", [
    "N", "NN", "NNN", "NNNN"
])
def test_id_register_multiple_letters(
        register: IDRegister,
        letter: str
) -> None:
    register.register(letter)
    assert letter in register._registered_ids


def test_id_register_reset(register: IDRegister) -> None:
    register.reset()
    assert len(register._registered_ids) == 0
    assert register._count == 0

@pytest.mark.parametrize("num,ids", [
    (1, ["A"]), (2, ["A", "B"]), (3, ["A", "B", "C"]),
    (4, ["A"]), (6, ["A", "B", "C", "D"]), (1, None),
    (6, None)
])
def test_id_record(num: int, ids: list[str] | None) -> None:
    entity = IDRecord(num, ids)
    assert entity.get_id() == ids
    if ids is None or num > len(ids):
        assert entity.num == num
    else:
        assert entity.num == len(ids)


@pytest.mark.parametrize("ids", [
    ["A"], ["A", "B"], ["A", "B", "C"], [], None
])
def test_id_record_assign(ids: list[str] | None) -> None:
    entity = IDRecord()
    entity.set_id(ids)
    if ids is not None and len(ids) == 0:
        assert entity.get_id() is None
        assert entity.num == 1
    else:
        assert entity.get_id() == ids

    if ids is None or len(ids) == 0:
        assert entity.num == 1
    else:
        assert entity.num == len(ids)


def test_id_record_remove() -> None:
    entity = IDRecord(seq_id=["A", "B", "C"])
    entity.remove_id()
    assert entity.get_id() is None


@pytest.mark.parametrize("seq_id, num", [
    (["A"], 1), (["A", "B"], 5), (["A", "B", "C"], 3),
])
def test_temporary_id(seq_id: list[str] | str | None, num: int) -> None:
    seq = ProteinSequence("AAQAA", seq_id=seq_id, num=num)
    input_file = InputFile()
    input_file.sequences.append(seq)
    input_file._prepare()
    assert seq.get_id() == seq_id
    assert len(seq.get_full_id_list()) == num
