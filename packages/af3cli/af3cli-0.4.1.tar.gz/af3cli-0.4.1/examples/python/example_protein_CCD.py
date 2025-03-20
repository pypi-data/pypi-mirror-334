"""
Example:
Human SIRT2 Histone Deacetylase
    - Protein Data Bank (PDB) Entry: 1J8F
    - Reference: https://www.rcsb.org/structure/1J8F
This simplified demonstration uses one monomer with one associated zinc ion for clarity.

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder, ProteinSequence, CCDLigand

# Define constants
FILENAME = "example_protein_ccd_python.json"
JOB_NAME = "example_protein_ccd_py_job"

INPUT_SEQUENCE_STR = (
    "GEADMDFLRNLFSQTLSLGSQKERLLDELTLEGVARYMQSERCRRVICLVGAGISTSAGIPDFRSPSTGLYDN"
    "LEKYHLPYPEAIFEISYFKKHPEPFFALAKELYPGQFKPTICHYFMRLLKDKGLLLRCYTQNIDTLERIAGLE"
    "QEDLVEAHGTFYTSHCVSASCRHEYPLSWMKEKIFSEVTPKCEDCQSLVKPDIVFFGESLPARFFSCMQSDFL"
    "KVDLLLVMGTSLQVQPFASLISKAPLSTPRLLINKEKAGQSDPFLGMIMGLGGGMDFDSKKAYRDVAWLGECD"
    "QGCLALAELLGWKKELEDLVRREHASIDAQS"
)

ZINC_ION_CCD =["ZN"]

# Create protein sequence object
sequence = ProteinSequence(INPUT_SEQUENCE_STR)

# Create ligand object
ligand = CCDLigand(ZINC_ION_CCD)

# Build input configuration for the job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(sequence)
input_builder.add_ligand(ligand)
internal_input = input_builder.build()

# Uncomment following line to generate output as JSON file
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())
