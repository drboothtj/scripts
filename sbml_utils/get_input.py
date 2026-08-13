'''
Extract network inputs from a draft metabolic model
        argv[1]: .sbml model
'''

from sys import argv
import cobra


def main(filepath: str) -> None:
        '''
        main routine
                arguments:
                        filepath: path to sbml file
        '''
        model = cobra.io.read_sbml_model(filepath)

        produced = set()
        consumed = set()

        for rxn in model.reactions:
            for met, coeff in rxn.metabolites.items():
                if coeff > 0:
                    produced.add(met.id)    # metabolite is produced
                elif coeff < 0:
                    consumed.add(met.id)    # metabolite is consumed

        starting_mets = consumed - produced

        print(f"Found {len(starting_mets)} network-inferred starting metabolites\n")

        for met_id in sorted(starting_mets):
            met = model.metabolites.get_by_id(met_id)
            name = met.name if met.name else ""
            formula = met.formula if met.formula else ""
            compartment = met.compartment if met.compartment else ""
            print(f"{met.id}\t{name}\t{formula}\t{compartment}\n")

FILEPATH = argv[1]
main(FILEPATH)

