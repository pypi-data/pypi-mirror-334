"""
Example:
fictive sequences and modifications derived from Protein Data Bank (PDB) Entry: "8AW3".

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder
from af3cli import CCDLigand
from af3cli import ProteinSequence, RNASequence, DNASequence
from af3cli import ResidueModification, NucleotideModification

# Define File and Job Name
FILENAME = "example_modifications_PTM.json"
JOB_NAME = "example_modifications_PTM_py_job"

# Define Protein Data
Protein_SEQUENCE_STR = (
    "MVQDTGKDTNLKGTAEANESVVYCDVFMQAALKEATCALEEGEVPVGCVLVKADSSTAAQAQAGDDLALQKLI"
    "VARGRNATNRKGHGLAHAEFVAVEELLRQATAGTSENIGGGGNSGAVSQDLADYVLYVVVEPCIMCAAMLLYN"
    "RVRKVYFGCTNPRFGGNGTVLSVHNSYKGCSGEDAALIGYESCGGYRAEEAVVLLQQFYRRENTNAPLGKRKR"
    "KD"
)
PROTEIN_MODIFICATIONS = [
    ResidueModification(mod_str="MCS", mod_pos=37),
    ResidueModification(mod_str="AGM", mod_pos=78),
    ResidueModification(mod_str="MLY", mod_pos=84),
    ResidueModification(mod_str="TPO", mod_pos=107),
    ResidueModification(mod_str="PTR", mod_pos=192),
]

# Define RNA Data
RNA_SEQUENCE_STR=(
    "GGCCGCUUAGCACAGUGGCAGUGCACCACUCUCGUAAAGUGGGGGUCGCGAGUUCGAUUCUCGCAGUGGCCUCCA"
)
RNA_MODIFICATIONS = [
    NucleotideModification(mod_str="2MG", mod_pos=2),
    NucleotideModification(mod_str="MA6", mod_pos=14),
    NucleotideModification(mod_str="5MU", mod_pos=22),
    NucleotideModification(mod_str="5MC", mod_pos=33),
]

# Define DNA Data
DNA_SEQUENCE_STR="ACGTTTCAGAGGCC"

DNA_MODIFICATIONS = [
    NucleotideModification(mod_str="6MA", mod_pos=1),
    NucleotideModification(mod_str="C34", mod_pos=2),
    NucleotideModification(mod_str="6OG", mod_pos=3),
    NucleotideModification(mod_str="3DR", mod_pos=4),
]

# Define Ligand Data
ZINC_ION_CCD = ["CA"]
LIGAND_NUM = 8

# Create Protein Sequence Object
protein_sequence = ProteinSequence(
    seq_str=Protein_SEQUENCE_STR,
    modifications=PROTEIN_MODIFICATIONS
)

# Create RNA Sequence Object
rna_sequence = RNASequence(
    seq_str=RNA_SEQUENCE_STR,
    modifications=RNA_MODIFICATIONS
)

# Create DNA Sequence Object
dna_sequence = DNASequence(
    seq_str=DNA_SEQUENCE_STR,
    modifications=DNA_MODIFICATIONS
)

# Create Ligand Object
ligand = CCDLigand(
    ligand_value=ZINC_ION_CCD,
    num=LIGAND_NUM
)

# Build Input Configuration for the Job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(protein_sequence)
input_builder.add_sequence(rna_sequence)
input_builder.add_sequence(dna_sequence)
input_builder.add_ligand(ligand)
internal_input = input_builder.build()

# Uncomment Following Line to Generate Output as JSON File
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())
