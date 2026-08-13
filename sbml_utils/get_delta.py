'''
This script calculates (delta) between the metabolites from two lists of draft metabolic models
    arguments:
        argv[1]: list_1
        argv[2]: list_2
'''
from sys import argv

import cobra
import glob

def get_metabolites(model_paths: str):
    '''
    '''
    all_metabolites = {}
    for model_path in model_paths:
        model = cobra.io.read_sbml_model(model_path)
        metabolites = {
            metabolite  for rxn in model.reactions for metabolite, coefficient in rxn.metabolites.items()
            if coefficient < 1 #only consumed metabolites
        }
        for metabolite in metabolites:
            if metabolite.id in all_metabolites:
                all_metabolites[metabolite.id]['count'] += 1
            else:
                all_metabolites[metabolite.id] = {
                    "name" : metabolite.name,
                    "formula" : metabolite.formula,
                    "compartment" : metabolite.compartment, #not used
                    "count" : 1
                }
    return all_metabolites



def main(list1: str, list2: str) -> None:
    '''
    main routine for get_delta
        arguments:
            list1: glob string for the first list of metabolic models (e.g. 'my_dir/*.sbml')
            list1: glob string for the second list of metabolic models (e.g. 'my_other_dir/*.sbml')
    '''
    list_1_paths = glob.glob(list1)
    list_2_paths = glob.glob(list2)

    metabolites_1 = get_metabolites(list_1_paths)
    metabolites_2 = get_metabolites(list_2_paths)

    print("\t".join([
                "id", "name", "formula",
                "count1", "count2",
                "percentage_1", "percentage_2",
                "delta", "abs_delta"
                ]))
    for _id in metabolites_1.keys() | metabolites_2.keys():
        name = metabolites_1.get(_id, metabolites_2.get(_id))['name'].replace(" ", "_")
        formula = metabolites_1.get(_id, metabolites_2.get(_id))['formula']
        
        count1 = metabolites_1.get(_id, {}).get("count", 0)
        count2 = metabolites_2.get(_id, {}).get("count", 0)
        percentage_1 = count1 / len(list_1_paths) * 100
        percentage_2 = count2 / len(list_2_paths) * 100
        delta = percentage_1 - percentage_2
        abs_delta = abs(percentage_1 - percentage_2)
        specificity = (percentage_1 ** 2) / (percentage_1 + percentage_2)

        print(
            "\t".join([
                _id, name, formula,
                str(count1), str(count2),
                str(percentage_1), str(percentage_2),
                str(delta), str(abs_delta), str(specificity)
                ])
        )

LIST_1 = argv[1]
LIST_2 = argv[2]
main(LIST_1, LIST_2)
