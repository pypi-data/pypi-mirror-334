from __future__ import annotations


class Atom(object):
    """
    Represents an atom with an entity ID, residue ID, and atom name.

    This class provides functionality to encapsulate atom data to
    be used in bond entries in AlphaFold3 input files.

    Attributes
    ----------
    eid : str
        The entity ID of the Atom.
    resid : int
        The residue ID of the Atom.
    name : str
        The name of the Atom.
    """
    def __init__(self, eid: str, resid: int, name: str):
        self.eid: str = eid
        self.resid: int = resid
        self.name: str = name

    def as_list(self) -> list[str | int]:
        """
        Converts the atom data into a list for the AlphaFold3 input file.

        Returns
        -------
        List
            A list containing the values of `eid`, `resid`, and `name`
            in the specified order.
        """
        return [self.eid, self.resid, self.name]

    @classmethod
    def from_string(cls, s: str) -> Atom:
        """
        Returns an Atom instance from a string representation.

        Parameters
        ----------
        s : str
            The string representation of the Atom in the
            format "eid:resid:name".

        Returns
        -------
        Atom
            An Atom instance parsed from the input string.
        """
        chain, num, atom_name = s.split(":")
        return cls(chain, int(num), atom_name)


class Bond(object):
    """
    Represents a bond entry between two atoms.

    The object is used to create a list of two atom lists
    for the AlphaFold3 input file.

    Attributes
    ----------
    atom1 : Atom
        The first atom involved in the bond.
    atom2 : Atom
        The second atom involved in the bond.
    """
    def __init__(self, atom1: Atom, atom2: Atom):
        self.atom1: Atom = atom1
        self.atom2: Atom = atom2

    def as_list(self) -> list[list]:
        """
        Converts the bond into a nested list representation.

        Returns
        -------
        List
            A nested list representation of `atom1` and `atom2`, where
            each is converted to its respective list form by calling
            their `as_list` methods.
        """
        return [self.atom1.as_list(), self.atom2.as_list()]

    @classmethod
    def from_string(cls, s: str) -> Bond:
        """
        Returns a Bond instance from a string representation.

        Parameters
        ----------
        s : str
            A string representation of the bond in the format
            "atom1-atom2", where `atom1` and `atom2` are
            string representations of the atoms in the
            format "eid:resid:name".

        Returns
        -------
        Bond
            A Bond instance parsed from the input string.
        """
        a1, a2 = s.split("-")
        return cls(Atom.from_string(a1), Atom.from_string(a2))
