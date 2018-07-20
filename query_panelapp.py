"""
query_panelapp.py
Author: Erik Waskiewicz
Date: 19-07-2018

Usage:
Takes panel unique ID and outputs a bed file of green genes in that
panel.
"""


import os
import sys
import json
import requests
import pandas as pd
import pybiomart
import datetime

BEDTOOLS_FILEPATH = '/Users/erik/Applications/bedtools2/bin/'
GENOME_FILEPATH = '/Users/erik/Projects/Trio_panelapp/hg19.genome'


# LIST ALL PANELS
def list_all_panels():
    # Extract full list from PanelApp API and store as dataframe
    url = "https://panelapp.genomicsengland.co.uk/WebServices/list_panels/"
    response = requests.get(url)
    data = response.json()
    #Extract info off all panels within panel app:
    all_panels = pd.io.json.json_normalize(data["result"])
    return(all_panels)


# LIST SPECIFIC PANEL INFORMATION
def get_panel(panel_id):
# Extract panel information from PanelApp API and save as dataframe
    url = ("https://panelapp.genomicsengland.co.uk/WebServices/get_panel/"
     + panel_id + "/")
    panel_response = requests.get(url)
    panel_data = panel_response.json()
    panel_df = pd.io.json.json_normalize(panel_data["result"]["Genes"])
    panel_meta = pd.io.json.json_normalize(panel_data["result"])
    panel_meta = panel_meta.drop(columns=['Genes', 'STRs'])
    print('Panel:         ' + panel_meta["SpecificDiseaseName"][0])
    print('Version:       ' + panel_meta["version"][0])
    print('PanelApp ID:   ' + panel_id)
    return(panel_df, panel_meta)


def get_gene_ids(panel_df, green=True, amber=False, red=False):
    # other option is 'NoList' if numbers dont add up
    dfs = []
    info = ''
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
    ids = pd.concat(dfs)
    info = info.rstrip(',')
    print('Genes:         ' + info)
    return(ids, info)


# SAVE SELECTION AS BED FILE
def save_as_bed(ensembl_ids, output_location, output_name, header):
    # biomart - loop through one by one as biomart cant deal with lots
    # of inputs (not sure what max is - cound speed this up using bigger
    # batches?)
    dataset = pybiomart.Dataset(
        name='hsapiens_gene_ensembl',
        host='http://grch37.ensembl.org'
    )

    csv_list = []
    for gene in ensembl_ids:
        query = dataset.query(
            attributes=['chromosome_name', 'start_position','end_position',
             'external_gene_name'], 
            filters={'link_ensembl_gene_id': gene}
        )
        csv_list += [query.to_csv(header=False, index=False, sep="\t")]

    # save csv file
    out = str(output_location) + str(output_name) + '.bed'
    csv_out = open(out, 'w')
    csv_out.write(str(header) + '\n')
    for item in sorted(csv_list):
        csv_out.write(item)
    csv_out.close()


def add_padding(output_location, output_name, header, padding=20):
    input_bed = str(output_location) + str(output_name) + '.bed'
    output_bed_file = (str(output_location) + str(output_name) 
        + '_pad' + str(padding) + '.bed')
    sort_command = (BEDTOOLS_FILEPATH + 'slopBed -i ' + input_bed + ' -g '
        + GENOME_FILEPATH + ' -b ' + str(padding))
    padded_bed = os.popen(sort_command).read()
    output_bed = open(output_bed_file, 'w')
    output_bed.write(str(header) + '\n')
    output_bed.write(padded_bed)
    output_bed.close()
    print('Padding:       ' + str(padding))


#----------------------------------------------------------------------
## CALL FUNCTIONS

#all_panels = list_all_panels()
#print(all_panels.to_string())
#print(all_panels.DiseaseGroup.unique())


print('Downloading panel...\n')

output_location = '/Users/erik/Desktop/panels/'
#panel = '285'
panel = str(sys.argv[1])
panel_df, panel_data = get_panel(panel)

# Extract list of Ensemble IDs and level of evidence in PanelApp, store
#  in dataframe
ensembl_ids, genes = get_gene_ids(panel_df)

output_name = (panel_data["SpecificDiseaseName"][0].replace(" ", "_") + "_v"
    + panel_data["version"][0] + '_' + genes.replace(',', '_').lower())

header = ('#PanelApp: ' + panel_data["SpecificDiseaseName"][0] + ' v' 
    + panel_data["version"][0] + '. PanelApp ID: ' + panel + '. Genes: ' 
    + genes + '. Group: ' + panel_data["DiseaseGroup"][0] + '. Subgroup: ' 
    + panel_data["DiseaseSubGroup"][0] + '. Date created ' 
    + str(datetime.date.today()))

save_as_bed(ensembl_ids, output_location, output_name, header)
add_padding(output_location, output_name, header)

print('\nDone.')
