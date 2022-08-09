#!/usr/bin/env conda run -n ct_extract_env python


import pandas as pd
import json


def parse_edges(data_folder):
    
    edges = pd.read_csv("ClinTrials_KG_edges_v01_2.csv", sep='\t')

    for index, row in edges.iterrows():
        id_dict = {}
        subject_dict = {}
        association_dict = {}
        object_dict = {}
        
        # id generated by concatenating the following: numbers from nctid, CUI of subject, CUI of object
        id_dict["_id"] = "{}_{}_{}".format(row["nctid"].split("nct")[1], row["subject"].split(':')[1], row["object"].split(':')[1])

        subject_dict["{}".format(row["subject"].split(':')[0])] = "{}".format(row["subject"].split(':')[1])
        subject_dict["name"] = row["subject_name"]
        # subject_dict["{}_semantic_types".format(row["subject"].split(':')[0])] = "TBD" # fix in next version
        subject_dict["type"] = "Disease"

        association_dict["predicate"] = "{}".format(row["predicate"].split(':')[1])
        # association_dict["provided_by"] = row["provided_by"]  # uncomment out when re-running full data
        # association_dict["provenance"] = row["provenance"]  # uncomment out when re-running full data
        association_dict["edge_attributes"] = []
        association_dict["edge_attributes"].append({"attribute_type_id":"biolink:original_knowledge_source", "value":"infores:clinicaltrials"})
        association_dict["edge_attributes"].append({"attribute_type_id":"clinicaltrials_id","value":row["nctid"]})

        object_dict["{}".format(row["object"].split(':')[0])] = "{}".format(row["object"].split(':')[1])
        object_dict["name"] = row["object_name"]
        object_dict["type"] = "Treatment"
        # object_dict["{}_semantic_types".format(row["object"].split(':')[0])] = "TBD" # fix in next version

        id_dict["subject"] = subject_dict
        id_dict["association"] = association_dict
        id_dict["object"] = object_dict 
        
        # yield the JSON one by one
        yield id_dict

    # print(json.dumps(id_dict, indent=2))

