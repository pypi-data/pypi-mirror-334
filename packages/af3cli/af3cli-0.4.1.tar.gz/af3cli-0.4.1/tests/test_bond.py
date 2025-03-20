import pytest

from af3cli.bond import Atom, Bond


@pytest.mark.parametrize("s,atom", [
    ("A:1:CA", Atom("A", 1, "CA")),
    ("B:2:O", Atom("B", 2, "O"))
])
def test_atom_from_str(s: str, atom: Atom) -> None:
    new_atom = Atom.from_string(s)
    assert new_atom.eid == atom.eid
    assert new_atom.resid == atom.resid
    assert new_atom.name == atom.name


@pytest.mark.parametrize("atom", [
    Atom("A", 1, "CA"),
    Atom("B", 2, "O")
])
def test_atom_as_list(atom: Atom) -> None:
    assert isinstance(atom.as_list(), list)
    assert atom.as_list() == [atom.eid, atom.resid, atom.name]


@pytest.mark.parametrize("atoms", [
    (Atom("A", 1, "CA"),
     Atom("B", 2, "O"))
])
def test_bond_init(atoms: tuple[Atom, Atom]) -> None:
    new_bond = Bond(*atoms)
    assert new_bond.atom1.eid == atoms[0].eid
    assert new_bond.atom2.eid == atoms[1].eid


@pytest.mark.parametrize("s,atoms", [
    ("A:1:CA-B:2:O",
     (Atom("A", 1, "CA"),
      Atom("B", 2, "O")))
])
def test_bond_from_str(s: str, atoms: tuple[Atom, Atom]) -> None:
    new_bond = Bond.from_string(s)
    assert new_bond.atom1.eid == atoms[0].eid
    assert new_bond.atom2.eid == atoms[1].eid


@pytest.mark.parametrize("bond", [
    Bond(Atom("A", 1, "CA"),
         Atom("B", 2, "O"))
])
def test_bond_as_list(bond: Bond) -> None:
    lst = bond.as_list()
    assert isinstance(lst, list)
    assert isinstance(lst[0], list)
    assert isinstance(lst[1], list)
    assert lst[0][0] == bond.atom1.eid
    assert lst[1][0] == bond.atom2.eid
