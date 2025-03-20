import os, datetime, re, json, copy
import traceback

import adagenes as ag
import adagenes.tools.load_dataframe
import adagenes.app.annotate
import adagenes.app.io
import adagenes.conf

from adagenes.app import generate_dataframe_from_dict

def recognize_column_types(list):
    column_type = None
    consistent_type = None

    for value in list:

        if value is None:
            continue
        elif value == "":
            continue

        try:
            val = int(value)
            column_type = 'integer'
            continue
        except:
            pass

        try:
            val = float(value)
            column_type = 'float'
            continue
        except:
            pass

        column_type = 'string'

        if column_type is not None:
            if column_type != consistent_type:
                if (column_type=="integer") and (consistent_type == "float"):
                    column_type = "float"
                elif ((column_type == "integer") or (column_type == "float")) and (consistent_type == "string"):
                    column_type = "string"

        consistent_type = column_type

    return column_type


def download_newest_file_as_csv(data_dir):
    infile = adagenes.app.io.find_newest_file(data_dir)
    outfile = infile + ".csv"

    # generate csv
    print("vcf to csv ",outfile)
    ag.process_file(infile, outfile, None)
    return outfile


def load_file(qid, data_dir, start_row=None, end_row=None):
    """

    :param qid:
    :param data_dir:
    :return:
    """
    data_dir = data_dir + "/" + qid
    #files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    #infile = data_dir + "/" + files[0]
    #print("data dir ",data_dir)
    infile = adagenes.app.io.find_newest_file(data_dir)

    if qid == "sample-vcf":
        infile = data_dir + ag.conf_reader.sample_file
    elif qid == "sample-protein":
        infile = data_dir + ag.conf_reader.sample_protein_file
    file_type = ag.get_file_type(infile)
    print("load file ",infile)

    bframe = ag.read_file(infile, start_row=start_row, end_row=end_row)
    #print(bframe.data)

    return bframe, file_type


def get_column_defs(output_format):
    pass



def get_previous_filters(previous_actions):
    previous_filters = []
    if isinstance(previous_actions, list):
        for action in previous_actions:
            if str(action).startswith("Filter:"):
                pattern = r'\[(.*?)\]'

                # Search for the pattern in the text
                match = re.search(pattern, action)

                # If a match is found, return the text within the brackets
                if match:
                    filter = match.group(1)
                    previous_filters.append([filter, action])
    return previous_filters



#qid, transform_output_format, transform_model, genome_version=genome_version, data_dir=data_dir

def transform_data(qid, transform_output_format, transform_model, genome_version=None, data_dir=None):
    """
    Annotate variant data with selected filters, and stores the annotated data in a new file

    :param qid:
    :param annotations:
    :param genome_version:
    :param data_dir:
    :param output_format:
    :return:
    """


    print("Transform ",transform_model)
    data_dir = adagenes.conf.read_config.__DATA_DIR__
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    if (transform_output_format == 'vcf') and (transform_model != {}):
        print("Transform to VCF ")

        if "gene" not in transform_model.keys():


            key = "transform-vcf"

            infile = adagenes.app.io.find_newest_file(data_dir)
            if qid == "sample-vcf":
                infile = data_dir + ag.conf_reader.sample_file
            if qid == "sample-protein":
                infile = data_dir + ag.conf_reader.sample_protein_file

            # infile = split_filename(infile)
            infile_name = ag.app.io.split_filename(infile)

            previous_actions = ag.app.io.load_log_actions(logfile)
            print("loaded logfile ", logfile)
            print("previous actions: ", previous_actions)

            out_filetype = "csv"
            if key == "transform-vcf":
                out_filetype = "vcf"
            print("out filetype ")

            annotation_key = 'Transformation:VCF'
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            if contains_substring is False:
                datetime_str = str(datetime.datetime.now())
                print("infile ", infile)
                outfile = infile_name + ".tf." + datetime_str + "." + '.' + out_filetype
                outfile = outfile.replace(" ", "_")
                outfile = outfile.replace(":", "-")

                magic_obj = adagenes.app.annotate.get_magic_obj(key, genome_version, transform_model=transform_model)
                ag.process_file(infile, outfile, magic_obj, output_format=out_filetype)

                ag.app.io.append_to_file(logfile, annotation_key + "(" + datetime_str + ")::" + outfile + '\n')

                print("File annotated: ", outfile)
            else:
                print("Annotation already found: ", annotation_key)
        else:
            # Protein2DNA conversion
            print("Protein to VCF")

            #magic_obj = adagenes.app.annotate.get_magic_obj("protein-to-gene")
            annotations = { 'protein-to-gene': True }
            mapping = { "gene": transform_model["gene"], "variant": transform_model["aa_exchange"] }
            adagenes.app.annotate.annotate_qid(qid, annotations,genome_version=genome_version, mapping=mapping)




def liftover_annotation(qid, genome_version, output_genome_version, data_dir=None, output_format='vcf'):
    """

    :param output_format:
    :param data_dir:
    :param qid:
    :param genome_version:
    :param output_genome_version:
    :return:
    """
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    infile = adagenes.app.io.find_newest_file(data_dir)
    if qid == "sample-vcf":
        infile = data_dir + ag.conf_reader.sample_file
    if qid == "sample-protein":
        infile = data_dir + ag.conf_reader.sample_protein_file

    infile_name = ag.app.io.split_filename(infile)
    datetime_str = str(datetime.datetime.now())
    outfile = infile_name + ".ann." + datetime_str + "." + output_format
    outfile = outfile.replace(" ", "_")
    outfile = outfile.replace(":", "-")

    magic_obj = ag.LiftoverAnnotationClient(genome_version = genome_version, target_genome=output_genome_version)
    #print("liftover annotation: ",genome_version," to ", output_genome_version,": ",infile, ": ",outfile)
    ag.process_file(infile, outfile, magic_obj)

    annotation_key = 'Liftover annotation:' + genome_version + " to " + output_genome_version + "(" + datetime_str + ")::" + outfile
    ag.app.io.append_to_file(logfile, annotation_key + '\n')


def liftover(qid, genome_version, output_genome_version, data_dir=None, output_format='vcf'):
    """

    :param output_format:
    :param data_dir:
    :param qid:
    :param genome_version:
    :param output_genome_version:
    :return:
    """
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    infile = adagenes.app.io.find_newest_file(data_dir)
    if qid == "sample-vcf":
        infile = data_dir + ag.conf_reader.sample_file
    if qid == "sample-protein":
        infile = data_dir + ag.conf_reader.sample_protein_file

    infile = ag.app.io.split_filename(infile)
    datetime_str = str(datetime.datetime.now())
    outfile = infile + ".ann." + datetime_str + "." + output_format
    outfile = outfile.replace(" ", "_")
    outfile = outfile.replace(":", "-")

    outfile = outfile.replace(genome_version,output_genome_version)

    magic_obj = ag.LiftoverClient(genome_version = genome_version, target_genome=output_genome_version)
    print("liftover: ",genome_version," to ", output_genome_version,": ",infile, ": ",outfile)
    ag.process_file(infile, outfile, magic_obj)

    annotation_key = 'Liftover:' + genome_version + " to " + output_genome_version + "(" + datetime_str + ")::" + outfile
    ag.app.io.append_to_file(logfile, annotation_key + '\n')


def is_filter(action):
    if str(action).startswith("Filter:"):
        return True
    else:
        return False

def compare_dictionaries(a, b):
    added = {}
    removed = {}

    # Check for added keys
    for key in b:
        if key not in a:
            added[key] = b[key]

    # Check for removed keys
    for key in a:
        if key not in b:
            removed[key] = a[key]

    return added, removed


def apply_filters(qid, filter_model, sort_model=None, data_dir=None, output_format='vcf', genome_version=None):
    """
        Apply AG Grid filterModel to the dataset.

        :param data
        :param filter_model
    """
    if sort_model is None:
        sort_model = {}

    print("Filters: ",filter_model)
    #bframe = load_file(qid, data_dir)
    #data = bframe.data
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    fallback_file = ""
    previous_actions = ag.app.io.load_log_actions(logfile)
    # print("loaded logfile ", logfile)
    print("previous actions: ", previous_actions)
    # find out if filter was removed
    previous_filters_list = get_previous_filters(previous_actions)
    print("previous filters ",previous_filters_list)

    columns_to_find = []
    columns_found = []
    first_filter_found = False
    reverse_data = False

    for i,prev_action in enumerate(reversed(previous_actions)):
        #if is_filter(prev_action):

            pattern = r';;.*?##'
            match = re.search(pattern, prev_action)

            if match:
                prev_filter_model = match.group(0)
                prev_filter_model = prev_filter_model.lstrip(";;").rstrip("##")
                print("prev filter model ",prev_filter_model)
                try:
                    prev_filter = json.loads(prev_filter_model)
                except:
                    print("Could not load JSON: ",prev_filter_model)
                    print(traceback.format_exc())
                    prev_filter = {}
            else:
                prev_filter = {}

            #if len(prev_action.split(";;")) > 1:
            #    prev_filter = json.loads(prev_action.split(";;")[1])
            #else:
            #    prev_filter = {}

            if first_filter_found is False:
                #print("Last entry ",prev_action)
                columns_to_find = list(prev_filter.keys())
                #print("prev action ", prev_action," columns to find: ",columns_to_find)
                #print("compare ",prev_filter," fm ",filter_model)

                if prev_filter != filter_model:
                    Added, removed = compare_dictionaries(prev_filter, filter_model)
                    if removed != {} :
                        reverse_data = True
                        print("Filter changed: Reverse data , filter model: ",filter_model," last saved model: ",prev_filter)
                else:
                    break
                first_filter_found = True

            #print("Search for last fitting model: ", filter_model, " saved model: ", prev_filter)
            if (prev_filter == filter_model) and (reverse_data is True):
                    print("Filter removed: ", prev_filter, ",", i, "Fallback to file: ", prev_action)
                    fallback_file = prev_action.split("::")[1]
                    fallback_file_nofilter = fallback_file.split(";;")
                    if len(fallback_file_nofilter)>1:
                        fallback_file = fallback_file_nofilter[0]
                    #print(fallback_file)
                    filter_model = prev_filter
                    #print("Loaded previous filter model: ", filter_model)
                    infile_name = ag.app.io.split_filename(fallback_file)
                    datetime_str = str(datetime.datetime.now())
                    outfile = infile_name.strip() + ".ann." + datetime_str + "." + output_format
                    outfile = outfile.replace(" ", "_")
                    outfile = outfile.replace(":", "-")
                    cmd = "cp -v " + fallback_file.strip() + " " + outfile
                    print(cmd)
                    os.system(cmd)
                    annotation_key = "Filter removed: " + "(" + datetime_str + ")::" + outfile + ";;" + json.dumps(
                        str(filter_model) + "##" + json.dumps(sort_model) )
                    ag.app.io.append_to_file(logfile, annotation_key + '\n')
                    break

    if (reverse_data is True) and (fallback_file == ""):
        filter_model = {}
        reversed(previous_actions)
        fallback_file = previous_actions[0].split("::")[1]
        print("no fitting prefilter found. Setting filter to zero ",fallback_file)
        infile_name = ag.app.io.split_filename(fallback_file)
        datetime_str = str(datetime.datetime.now())
        outfile = infile_name.strip() + ".ann." + datetime_str + "." + output_format
        outfile = outfile.replace(" ","_")
        outfile = outfile.replace(":","-")
        print("outfile ",outfile)
        print("ff ",fallback_file)
        cmd = "cp -v " + fallback_file.strip() + " " + outfile
        print(cmd)
        os.system(cmd)

        annotation_key = "Filter removed: " + "(" + datetime_str + ")::" + outfile + ";;" + json.dumps(filter_model) + \
            json.dumps(sort_model)
        ag.app.io.append_to_file(logfile, annotation_key + '\n')

            #for pcol in columns_to_find:
            #    if pcol in filter_model.keys():
            #        if prev_filter[pcol] == filter_model[pcol]:
            #            columns_to_find.pop(pcol)


        #if len(columns_to_find) > 0:
        #        print("Filter removed: ", prev_filter, ",", i, "Fallback to file: ", previous_actions[i+1])
        #        fallback_file = previous_actions[i+1].split("::")[1]
        #        fallback_file_nofilter = fallback_file.split(";;")
        #        if len(fallback_file_nofilter)>1:
        #            fallback_file = fallback_file_nofilter[0]
        #        print(fallback_file)
        #        # load previous filters
        #        pfilter = previous_actions[i+1].split(";;")
        #        if len(pfilter) > 1:
        #            prev_filter_str = json.loads(previous_actions[i-1].split(";;")[1])
        #        else:
        #            prev_filter_str = {}
        #        filter_model = prev_filter_str
        #        print("Loaded previous filter model: ", filter_model)

    #for filter_item in filter_model.keys():
    #    column = filter_item
    #    filter_data = filter_model(filter_item)
    for column, filter_data in filter_model.items():
        #print("column ",column,", ",filter_data)
        filter_type = filter_data.get("filterType")

        #if fallback_file == "":
        infile = adagenes.app.io.find_newest_file(data_dir)
        #else:
        #    infile = fallback_file
        if qid == "sample-vcf":
            infile = data_dir + ag.conf_reader.sample_file
        if qid == "sample-protein":
            infile = data_dir + ag.conf_reader.sample_protein_file

        #print("Filter: ", filter_type, " ", qid, ": ",infile)
        infile_name = ag.app.io.split_filename(infile)

        magic_obj = adagenes.app.annotate.get_magic_obj("filter_" + filter_type, None)
        filter = []
        filter_value = filter_data["filter"]
        filter.append(column)
        filter.append(filter_value)
        filter_type = filter_data['type']
        filter.append(filter_type)
        annotation_key = 'Filter:' + str(filter) #+ "(" + datetime_str + ")"

        if annotation_key not in previous_actions:
            datetime_str = str(datetime.datetime.now())
            print("infile ", infile)
            outfile = infile_name + ".ann." + datetime_str + "." + output_format
            outfile = outfile.replace(" ", "_")
            outfile = outfile.replace(":", "-")
            datetime_str = str(datetime.datetime.now())
            #outfile = infile + datetime_str + "_" + ".ann." + output_format
            annotation_key = annotation_key + "(" + datetime_str + ")::" + outfile + ";;" + json.dumps(filter_model) + \
                "##" + json.dumps(sort_model)

            magic_obj.filter = filter
            print(magic_obj.filter)
            ag.process_file(infile, outfile, magic_obj)
            print("Filtered file: ", outfile)

            ag.app.io.append_to_file(logfile, annotation_key + '\n')
        else:
            print("Filter already found: ",annotation_key)


        #if filter_type == "text":
        #    data = [
        #        row
        #        for row in data
        #        if str(filter_data["filter"]).lower() in str(row[column]).lower()
        #    ]
        #elif filter_type == "number":
        #    filter_value = filter_data["filter"]
        #    if filter_data["type"] == "equals":
        #        data = [row for row in data if row[column] == filter_value]
        #    elif filter_data["type"] == "greaterThan":
        #        data = [row for row in data if row[column] > filter_value]
        #    elif filter_data["type"] == "lessThan":
        #        data = [row for row in data if row[column] < filter_value]
    #return data

    return filter_model


def apply_sorting(qid, sort_model, filter_model=None, data_dir=None):
    """
    Apply AG Grid sortModel to the dataset.

    :param data:
    :param sort_model:
    """
    if filter_model is None:
        filter_model = {}

    #print("Sort: ",sort_model)

    #bframe = load_file(qid, data_dir)
    #data = bframe.data
    #data = generate_dataframe_from_dict(data)
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    if sort_model:
        sort_found = False
        for sort in reversed(sort_model):  # AG Grid supports multi-column sorting
            if sort["sort"] is not None:
                sort_found = True
                if sort["sort"] == "asc":
                    asc = True
                else:
                    asc = False

                infile = adagenes.app.io.find_newest_file(data_dir)
                infile_name = ag.app.io.split_filename(infile)
                print("load sorting file ",infile)
                df, header_lines = adagenes.tools.load_dataframe.load_dataframe(infile)
                cols_orig = copy.deepcopy(df.columns)
                print("loaded df ", df)

                print("Sort ",sort["field"], ": ",sort["sort"],", ")
                #print("Order: ", data)
                column = sort["colId"]
                order = sort["sort"]
                reverse = order == "desc"
                #data.sort(key=lambda x: x[column], reverse=reverse)
                #data.sort(key=lambda x: (math.isnan(x[column]) if isinstance(x[column], float) else False, x[column]),
                #          reverse=reverse)

                #data.sort(key=lambda x: (x.get(column, None) is None, x.get(column, None)), reverse=reverse)
                columns_lower = [x.lower() for x in list(df.columns)]
                df.columns = columns_lower

                df = df.sort_values(by=column, ascending = asc)

        if sort_found is False:
            pass
            #infile = find_newest_file(data_dir)
            #infile_name = split_filename(infile)
            #df = adagenes.tools.load_dataframe.load_dataframe(infile)
            #cols_orig = copy.deepcopy(df.columns)
        else:
            datetime_str = str(datetime.datetime.now())
            df.columns = cols_orig
            output_format="vcf"

            outfile = infile_name + ".ann." + datetime_str + "." + output_format
            outfile = outfile.replace(" ", "_")
            outfile = outfile.replace(":", "-")
            print("sorted file outfile ",outfile)
            adagenes.tools.load_dataframe.dataframe_to_vcf(df, header_lines, outfile)

            # Add log file entry
            annotation_key = "Sort model: " + "(" + datetime_str + ")::" + outfile + ";;" + json.dumps(
                filter_model) + "##" + json.dumps(sort_model)
            ag.app.io.append_to_file(logfile, annotation_key + '\n')

    #return data


def generate_table_data_from_bframe(bframe, output_format=None):
    column_defs = []
    table_data = []

    #print("output format ",output_format)
    columns = []

    if output_format == "vcf":
        table_data = []

        columns = ['CHROM', 'POS','ID','REF','ALT','QUAL','FILTER']
        column_defs = [
            {'headerName': 'CHROM', 'field': 'chrom', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'POS', 'field': 'pos', 'filter': "agNumberColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'ID', 'field': 'id', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'REF', 'field': 'ref', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'ALT', 'field': 'alt', 'filter': "agTextColumnFilter", 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'QUAL', 'field': 'qual', 'filter': 'agNumberColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200},
            {'headerName': 'FILTER', 'field': 'filter', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true',
             'minWidth': 200}
        ]

        for var in bframe.data.keys():
            # base VCF columns
            if "variant_data" in bframe.data[var]:
                if "ID" in bframe.data[var]["variant_data"]:
                    id_data = bframe.data[var]["variant_data"]['ID']
                else:
                    id_data = "."

                if "QUAL" in bframe.data[var]["variant_data"]:
                    qual_data = bframe.data[var]['variant_data']['QUAL']
                else:
                    qual_data = '.'

                if "FILTER" in bframe.data[var]["variant_data"]:
                    filter_data = bframe.data[var]['variant_data']['FILTER']
                else:
                    filter_data = '.'

            #print(bframe.data[var])

            dc = {
                'chrom': bframe.data[var]["variant_data"]["CHROM"],
                'pos': bframe.data[var]["variant_data"]["POS"],
                'id': id_data,
                'ref': bframe.data[var]["variant_data"]["REF"],
                'alt': bframe.data[var]["variant_data"]["ALT"],
                'qual': qual_data,
                'filter': filter_data
            }

            # Preexisting features
            #print(bframe.data)
            info_features = bframe.data[var]["info_features"].keys()
            #print("INFO Features ",info_features)
            #print(bframe.data[var]["info_features"])
            for inf in info_features:
                column_type = recognize_column_types([bframe.data[var]["info_features"][inf]])
                if column_type == "float":
                    filter_type = "agNumberColumnFilter"
                elif column_type == "integer":
                    filter_type = "agNumberColumnFilter"
                else:
                    filter_type = "agTextColumnFilter"

                column_id = inf.lower()
                dc[column_id] = bframe.data[var]["info_features"][inf]

                inf_column = { 'headerName': inf, 'field': column_id, 'filter': filter_type, 'floatingFilter': 'true',
                               'minWidth': 200}

                if column_id not in columns:
                    column_defs.append(inf_column)
                    columns.append(column_id)

            table_data.append(dc)
        #print("Columns ",columns)

    else:

        for var in bframe.data.keys():
            # base VCF columns
            if "variant_data" in bframe.data[var]:
                if "ID" in bframe.data[var]["variant_data"]:
                    id_data = bframe.data[var]["variant_data"]['ID']
                else:
                    id_data = "."

                if "QUAL" in bframe.data[var]["variant_data"]:
                    qual_data = bframe.data[var]['variant_data']['QUAL']
                else:
                    qual_data = '.'

                if "FILTER" in bframe.data[var]["variant_data"]:
                    filter_data = bframe.data[var]['variant_data']['FILTER']
                else:
                    filter_data = '.'

            #print(bframe.data[var])

            dc = {}

            # Preexisting features
            #print(bframe.data)
            #info_features = bframe.data[var]["info_features"].keys()
            info_features = bframe.data[var].keys()
            #print("INFO Features ",info_features)
            #print(bframe.data[var]["info_features"])
            for inf in info_features:
                column_type = recognize_column_types([bframe.data[var][inf]])
                if column_type == "float":
                    filter_type = "agNumberColumnFilter"
                elif column_type == "integer":
                    filter_type = "agNumberColumnFilter"
                else:
                    filter_type = "agTextColumnFilter"



                inf_column = { 'headerName': inf, 'field': inf.lower(), 'filter': filter_type, 'floatingFilter': 'true',
                               'minWidth': 200}

                column_id = inf.lower()
                #dc[column_id] = bframe.data[var]["info_features"][inf]
                dc[column_id] = bframe.data[var][inf]

                #if inf not in columns:
                if column_id not in columns:
                    column_defs.append(inf_column)
                    columns.append(column_id)

            table_data.append(dc)

    #print("Columns ", columns)
    #print("Columns defs: ",column_defs)
    #print(table_data)
    return column_defs, table_data


def analyze_uploaded_file(qid, data_dir = None,
                          start_row=None, end_row=None,
                          genome_version="hg38",
                          output_genome_version='',
                          output_format="vcf", annotate=None,
                          sort_model=None, filter_model = None,
                          transform_output_format = None,
                          transform_model = None):
    """

    :param qid:
    :param data_dir:
    :param genome_version:
    :param output_format:
    :return:
    """

    # Liftover annotation
    if genome_version != "hg38":
        # test if newest file is hg38
        #data_dir = data_dir + "/" + qid
        infile = adagenes.app.io.find_newest_file(data_dir + "/" + qid)
        newest_file_genome_version = infile.split("_")[0].split("/")[-1]

        #print("newest genome version: ",newest_file_genome_version)

        if (newest_file_genome_version == "hg19") or (newest_file_genome_version == "t2t"):
            logfile = data_dir + '/qid' + '/log.txt'
            previous_actions = ag.app.io.load_log_actions(logfile)
            annotation_key = 'Liftover annotation:' + newest_file_genome_version + " to hg38"
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            #print(logfile,"::",annotation_key,"::",previous_actions)
            #print("contains ",str(contains_substring))
            if contains_substring is False:
                print("automated liftover annotation:", newest_file_genome_version + " to hg38")
                liftover_annotation(qid, newest_file_genome_version, "hg38", data_dir=data_dir)

    # Liftover
    print("Genome ",genome_version,", output ", output_genome_version)
    if (output_genome_version != '') and (output_genome_version != genome_version):
        print("Liftover: ",genome_version," to ",output_genome_version)
        liftover(qid, genome_version, output_genome_version, data_dir=data_dir)

    # Transform
    if transform_model is not None:
        transform_data(qid, transform_output_format, transform_model, genome_version=genome_version, data_dir=data_dir)

    # Apply filtering
    if filter_model is not None:
        filter_model = apply_filters(qid, filter_model, sort_model=sort_model, data_dir=data_dir)

    # Apply sorting
    if sort_model is not None:
        apply_sorting(qid, sort_model, filter_model=filter_model, data_dir=data_dir)

    # Annotate
    if annotate is not None:
        if len(list(annotate.keys())) > 0:
            #adagenes.app.annotate.annotate_qid(qid, annotate, genome_version=genome_version, data_dir=data_dir)
            #adagenes.app.annotate.annotate_qid_chunks(qid, annotate, genome_version=genome_version, data_dir=data_dir)
            adagenes.app.annotate.annotate_qid_chunks_parallel(qid, annotate, genome_version=genome_version, data_dir=data_dir)

    # load saved file
    print("load file ",qid," ",data_dir)
    bframe, file_type = load_file(qid, data_dir, start_row=start_row, end_row=end_row)
    max_rows = bframe.max_variants


    column_defs, table_data = generate_table_data_from_bframe(bframe, output_format=file_type)


    #print("loaded file ", table_data)
    #print("column defs ",column_defs)
    #print("max rows ",max_rows)
    return column_defs, table_data, max_rows, filter_model, output_genome_version

def analyze_search():

    column_defs = []
    table_data = []

    return column_defs, table_data

