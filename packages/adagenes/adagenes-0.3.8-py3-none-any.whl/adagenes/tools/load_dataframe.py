import pandas as pd

def split_key_value_pairs(df, column_index):
    key_value_column = df.iloc[:, column_index - 1]

    new_columns = {}

    for index, row in key_value_column.items():
        pairs = row.split(';')

        row_dict = {}
        for pair in pairs:
            elements = pair.split('=')
            if len(elements) > 1:
                key, value = pair.split('=')
                row_dict[key] = value

        new_columns[index] = row_dict

    new_df = pd.DataFrame.from_dict(new_columns, orient='index')
    result_df = pd.concat([df, new_df], axis=1)
    return result_df


def load_dataframe(infile):

    if infile.endswith("vcf"):
        lines = []
        columns = []
        header_lines = []
        with open(infile, 'r') as file:
            for line in file:
                if line.startswith("##"):
                    header_lines.append(line.strip())
                elif line.startswith("#"):
                    if line.startswith(("#CHROM")):
                        columns = line.lstrip('#').strip().split("\t")
                        header_lines.append(line.strip())
                else:
                    #lines = [line for line in file if not line.startswith('#')]
                    lines.append(line.strip())

        # Create a DataFrame from the lines
        df = pd.DataFrame([line.strip().split('\t') for line in lines])

        # Assign column names based on the header line (assuming the header is the first non-comment line)
        #header = lines[0].strip().split('\t')
        print("header ",columns, " shape ",df.shape)
        if columns != []:
            df.columns = columns
        else:
            df.columns = ["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"]

        #print("df ",df.columns, "data: ",df)
        df = split_key_value_pairs(df, 8)
        df = df.fillna('')

        return df, header_lines

def dataframe_to_vcf(df, header_lines, output_file):
    """
    Converts a pandas DataFrame into a VCF file.

    Parameters:
        df (pd.DataFrame): Input DataFrame. First 7 columns correspond to VCF required columns,
                           and additional columns correspond to INFO fields.
        output_file (str): Path to the output VCF file.
    """

    print("sorted df to file: ",df)

    # Open the output file and write the header
    with open(output_file, 'w') as f:
        for line in header_lines:
            f.write(line + '\n')

        for index, row in df.iterrows():
            # Extract first 7 mandatory VCF columns
            chrom, pos, vid, ref, alt, qual, filt = row.iloc[:7]

            # Build the INFO field from the remaining columns
            info_fields = []
            for col in df.columns[7:]:
                if col != "INFO":
                    #print("info features ", col, ": ", row[col])
                    value = row[col]
                    #if pd.notna(value):  # Only include non-NaN values
                    info_fields.append(f"{col}={value}")

            info = "" if not info_fields else ";".join(info_fields)

            # Write the VCF row
            f.write(f"{chrom}\t{pos}\t{vid}\t{ref}\t{alt}\t{qual}\t{filt}\t{info}\n")
