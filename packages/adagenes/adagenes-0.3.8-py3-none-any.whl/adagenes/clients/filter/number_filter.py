# if filter_type == "text":
#    data = [
#        row
#        for row in data
#        if str(filter_data["filter"]).lower() in str(row[column]).lower()
#    ]
# elif filter_type == "number":
#    filter_value = filter_data["filter"]
#    if filter_data["type"] == "equals":
#        data = [row for row in data if row[column] == filter_value]
#    elif filter_data["type"] == "greaterThan":
#        data = [row for row in data if row[column] > filter_value]
#    elif filter_data["type"] == "lessThan":
#        data = [row for row in data if row[column] < filter_value]

import copy
import traceback
import pandas as pd
import adagenes
from adagenes.clients import client
import adagenes as ag


class NumberFilter(client.Client):
    """
    Filters biomarker data according to a defined feature value, filters only exact matches
    """

    def __init__(self, filter=None, error_logfile=None):
        """

        :param filter:
        :param error_logfile:
        """
        self.filter = filter

        self.qid_key = "q_id"
        self.error_logfile = error_logfile

    def process_data(self, bframe):
        """
        Filters biomarkers according to specified feature values

        Filter arguments are defined as a list in the filter argument, consisting of a property, a defined value, and an operator.

        Example: Filter all variants according to allele frequency
        filter = ['AC', '0.1', '>']

        :param bframe: AdaGenes biomarker frame object
        :param filter: List of arguments to define the filter
        :param inv:
        :return:
        """
        is_biomarker = False
        if isinstance(bframe, dict):
            biomarker_data = bframe
        elif isinstance(bframe, adagenes.BiomarkerFrame):
            biomarker_data = bframe.data
            is_biomarker = True
        else:
            biomarker_data = bframe
        biomarker_data_new = {}

        if (self.filter is None) and (isinstance(bframe, ag.BiomarkerFrame)):
            self.filter = bframe.filter

        #print("NUmber filter: ",self.filter)
        dc_cols = {}


        for var in biomarker_data:
            if self.filter is not None:
                if isinstance(self.filter, list):
                    try:
                        feature = self.filter[0]
                        operator = self.filter[2]
                        val_comp = float(self.filter[1])
                        df = pd.json_normalize(biomarker_data[var])
                        columns_lower = []
                        for key in df.columns:
                            dc_cols[key.lower()] = key
                            columns_lower.append(key.lower())

                        if feature not in columns_lower:
                            if "variant_data." + feature in columns_lower:
                                feature = "variant_data." + feature
                            elif "info_features."+feature in columns_lower:
                                feature = "info_features." + feature

                        if feature in columns_lower:
                            if operator == ">":
                                val = float(df[dc_cols[feature]])
                                if val > val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                                else:
                                    pass
                            elif operator == "<":
                                pass
                            elif operator == "equals":
                                val_float = float(df[dc_cols[feature]])
                                if val_float == val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                                elif str(self.filter[1]) in str(df[dc_cols[feature]]):
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "Equals":
                                val_float = float(df[dc_cols[feature]])
                                if val_float == val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "notEqual":
                                val_float = float(df[dc_cols[feature]])
                                if val_float != val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "greaterThan":
                                val_float = float(df[dc_cols[feature]])
                                if val_float > val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "greaterThanOrEqual":
                                val_float = float(df[dc_cols[feature]])
                                if val_float >= val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "lessThan":
                                val_float = float(df[dc_cols[feature]])
                                if val_float < val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                            elif operator == "lessThanOrEqual":
                                val_float = float(df[dc_cols[feature]])
                                if val_float <= val_comp:
                                    biomarker_data_new[var] = biomarker_data[var]
                    except:
                        print(traceback.format_exc())
                else:
                    print("Error: Filter must be a list")

        if is_biomarker:
            bframe_new = copy.deepcopy(bframe)
            bframe_new.data = copy.deepcopy(biomarker_data_new)
            return bframe_new

        return biomarker_data_new
