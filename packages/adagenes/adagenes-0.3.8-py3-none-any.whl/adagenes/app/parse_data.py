import base64
import datetime
import io
#import magic
import adagenes as ag
from dash import Dash, dcc, html


def parse_contents(contents, filename, date, output_format=None, reference_genome=None):
    """
    Main function for processing file uploads

    :param contents:
    :param filename:
    :param date:
    :return:
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        label=filename
        sep="\t"
        file_type="csv"
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            #mime = magic.Magic(mime=True)
            #file_type = mime.from_file(io.StringIO(decoded.decode('utf-8')))
            #if file_type == 'text/tab-separated-values':
            #    sep="\t"
            #else:
            #    sep=","

            #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),sep=",")
            file_type = "csv"
            sep=","
        elif "vcf" in filename:
            #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep="\t")
            file_type = "vcf"
            sep="\t"
        elif "maf" in filename:
            file_type="maf"
            sep="\t"
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            #df = pd.read_excel(io.BytesIO(decoded))
            file_type="xlsx"
            sep="\t"
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]), None

    #bframe = av.dataframe_to_bframe(df, filename)
    bframe = ag.read_file(io.StringIO(decoded.decode('utf-8')), input_format=file_type, sep=sep)
    print("loaded bframe: ",bframe)
    df_new = ag.bframe_to_app_dataframe(bframe, output_format = output_format)

    return ag.app.display_table(df_new,label, reference_genome, output_format)
