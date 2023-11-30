'''
Converts a SMILES object to .mol2 format. This is required for docking analysis with SwissDock.
'''
from rdkit import Chem
from sys import argv

smiles_string = argv[1]

rd_molecule = Chem.MolFromSmiles(smiles_string)
mol2_molecule = Chem.MolToMolBlock(rd_molecule)

with open("my_molecule.mol2", "w") as my_file:
	my_file.write(mol2_molecule)

