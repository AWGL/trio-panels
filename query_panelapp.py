"""
query_panelapp.py
Author:  Erik Waskiewicz
Date:    23-07-2018
Version: 0.1.0

Usage:
Takes panel unique ID and outputs a bed file of green genes in that
panel.
"""


## IMPORT PACKAGES ----------------------------------------------------


import os
import sys
import json
import requests
import pandas as pd
import pybiomart
import datetime


## SET FILEPATHS ------------------------------------------------------


BEDTOOLS_FILEPATH = '/Users/erik/Applications/bedtools2/bin/'
GENOME_FILEPATH = '/Users/erik/Projects/Trio_panelapp/hg19.genome'
OUTPUT_LOCATION = '/Users/erik/Desktop/panels/'


## DEFINE FUNCTIONS ---------------------------------------------------


def list_all_panels():
    '''
    Extract full list of panels from PanelApp API and store as a pandas
    dataframe.

    NOTE: NOT CURRENTLY USED - can be used in future to make a tool to
    select a panel through a GUI, rather than inputting the panel ID
    through the command line.
    '''

    # Query PanelApp API
    url = "https://panelapp.genomicsengland.co.uk/WebServices/list_panels/"
    response = requests.get(url)
    data = response.json()

    # Extract info of all panels within panel app
    all_panels = pd.io.json.json_normalize(data["result"])
    return(all_panels)


def get_panel(panel_id):
    '''
    Input PanelApp panel ID, extract panel information from PanelApp
    API, split the response into a list of genes and a list of meta
    data and return both as pandas dataframes.
    '''

    # Query PanelApp API
    url = ("https://panelapp.genomicsengland.co.uk/WebServices/get_panel/"
     + panel_id + "/")
    panel_response = requests.get(url)
    panel_data = panel_response.json()

    # Filter response for gene list or meta data
    panel_df = pd.io.json.json_normalize(panel_data["result"]["Genes"])
    panel_meta = pd.io.json.json_normalize(panel_data["result"])
    panel_meta = panel_meta.drop(columns=['Genes', 'STRs'])

    # Print summary to screen and return dataframes
    print('Panel:         ' + panel_meta["SpecificDiseaseName"][0])
    print('Version:       ' + panel_meta["version"][0])
    print('PanelApp ID:   ' + panel_id)

    return(panel_df, panel_meta)


def get_gene_ids(panel_df, green=True, amber=False, red=False):
    '''
    Take pandas dataframe of specific panel gene information and filter
    based on whether each gene is a green, amber or red gene. Return
    pandas dataframe of filtered genes and an info string to add to the
    bed file header.

    NOTE: There is another option other than green, amber and red -
    'NoList'. This might mean that numbers dont add up if comaring to
    the PanelApp website.
    '''

    # Make empty variables to collect data
    dfs = []
    info = ''

    # If setting is true, filter dataframe and add to variables
    if green == True:
        green_ids = (panel_df
            [panel_df.LevelOfConfidence == 'HighEvidence']
            .loc[:,'EnsembleGeneIds']
        )
        dfs += [green_ids]
        info += 'Green,'

    if amber == True:
        amber_ids = (panel_df
            [panel_df.LevelOfConfidence == 'ModerateEvidence']
            .loc[:,'EnsembleGeneIds']
        )
        dfs += [amber_ids]
        info += 'Amber,'

    if red == True:
        red_ids = (panel_df
            [panel_df.LevelOfConfidence == 'LowEvidence']
            .loc[:,'EnsembleGeneIds']
        )
        dfs += [red_ids]
        info += 'Red,'

    # Combine dataframes and remove trailing comma from info
    ids = pd.concat(dfs)
    info = info.rstrip(',')

    print('Genes:         ' + info)
    return(ids, info)


def save_as_bed(ensembl_ids, output_location, output_name, header):
    '''
    Take in pandas dataframe of 1 column containing a list of Ensembl
    IDs, use the pybiomart package to query each Ensembl ID one by one
    and return a BED file row for each one. Save the output as a .BED
    file with a header containing the panel information.

    NOTE: Loop through one by one as biomart cant deal with lots of
    inputs (not sure what max is - cound speed this up using batches?)
    '''

    # Load in pybiomart dataset - GRCh37
    dataset = pybiomart.Dataset(
        name='hsapiens_gene_ensembl',
        host='http://grch37.ensembl.org'
    )

    # Query each ID one at a time and add to list
    bed_list = []
    for gene in ensembl_ids:
        query = dataset.query(
            attributes=['chromosome_name', 'start_position','end_position',
             'external_gene_name'], 
            filters={'link_ensembl_gene_id': gene}
        )
        bed_list += [query.to_csv(header=False, index=False, sep="\t")]

    # Save BED file
    out = str(output_location) + str(output_name) + '.bed'
    csv_out = open(out, 'w')
    csv_out.write(str(header) + '\n')
    for item in sorted(bed_list):
        csv_out.write(item)
    csv_out.close()


def add_padding(output_location, output_name, header, padding=20):
    '''
    Take in BED file and apply padding using BEDTools slop tool,
    outputs identical BED file with added padding.
    '''

    # Define inputs and outputs
    input_bed = str(output_location) + str(output_name) + '.bed'
    output_bed_file = (str(output_location) + str(output_name) 
        + '_pad' + str(padding) + '.bed')

    # Run padding command
    sort_command = (BEDTOOLS_FILEPATH + 'slopBed -i ' + input_bed + ' -g '
        + GENOME_FILEPATH + ' -b ' + str(padding))
    padded_bed = os.popen(sort_command).read()

    # Save output
    output_bed = open(output_bed_file, 'w')
    output_bed.write(str(header) + '|Padding: ' + str(padding) + 'bp \n')
    output_bed.write(padded_bed)
    output_bed.close()
    print('Padding:       ' + str(padding))


## CALL FUNCTIONS -----------------------------------------------------


print('Downloading panel...\n')

# Take panel ID as argument, get panel gene list and meta data
panel = str(sys.argv[1])
panel_df, panel_data = get_panel(panel)

# Extract list of Ensemble IDs and filter on level of evidence
ensembl_ids, genes = get_gene_ids(panel_df)  # Change green/amber/red

# Make output filename from variables
output_name = (panel_data["SpecificDiseaseName"][0].replace(" ", "_") + "_v"
    + panel_data["version"][0] + '_' + genes.replace(',', '_').lower())

# Make BED file header from variables
header = ('#PanelApp panel: ' + panel_data["SpecificDiseaseName"][0] + ' v' 
    + panel_data["version"][0] + '|PanelApp ID: ' + panel + '|Genes: ' 
    + genes + '|Group: ' + panel_data["DiseaseGroup"][0] + '|Subgroup: ' 
    + panel_data["DiseaseSubGroup"][0] + '|Date created: ' 
    + str(datetime.date.today()))

# Make BED file and add padding
save_as_bed(ensembl_ids, OUTPUT_LOCATION, output_name, header)
add_padding(OUTPUT_LOCATION, output_name, header)  # Change padding

print('\nDone.')
