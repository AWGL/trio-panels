"""
apply_panel_trios.py
Author: Erik Waskiewicz
Date: 26-04-2018

Usage:
Takes trio variant report txt file outputted from VariantRepoterSpark
as first argument, panel to be applied as second argument:
<path>/python apply_panel_trios.py <path/trio_variant_report.txt> 
  <path/panel_to_be_applied.bed>

Outputs a txt file in the same format as the original variant report 
with panel applied. Output is saved in the same folder as the original
variant report with the panel appended to the file name.
"""


import csv
import os
import sys
import datetime

BEDTOOLS_FILEPATH = '/Users/erik/Applications/bedtools2/bin/'


# inputs - 
def load_variables():
    '''
    Takes in sys arg 1 as report filepath
    '''
    report_input = sys.argv[1]
    print('Report:      ' + str(sys.argv[1]))
    panel_input = sys.argv[2:]
    print('Panel(s):    ' + str(sys.argv[2:]))
    # bedtool input string
    bedtools_input = ''
    for panel in panel_input:
        bedtools_input += str(panel + ' ')
    # extract data from inputs
    report_path = report_input.rstrip(report_input.split('/')[-1])
    panel_name = ''
    for panel in panel_input:
        panel_name += panel.split('/')[-1].rstrip('.bed') + '_'
    panel_name = panel_name.rstrip('_')
    return(report_input, panel_input, bedtools_input, report_path, panel_name)


def make_report_bed(report_input, report_path):
    # open file to save bed file of variants in report
    report_bed_filepath = report_path + 'report_bed.bed'
    report_bed = open(report_bed_filepath, 'w')
    # extract variants from variant report and make bed file and save 
    # to file
    with open(report_input) as report:
        results = csv.reader(report, delimiter='\t')
        for line in results:
            if line[0][0] != '#':
                variant = line[2].split(':')
                report_bed.write(variant[0] + "\t"
                    + str(int(variant[1].strip('AGTC>')) - 1)
                    + "\t" + variant[1].strip('AGTC>') + "\t"
                    + line[2] + "\n")
    report_bed.close()
    # sort bed file and save to a different file
    sort_command = BEDTOOLS_FILEPATH + 'sortBed -i ' + report_bed_filepath
    results_sorted = os.popen(sort_command).read()
    report_bed_sorted_filepath = report_path + 'report_bed_sorted.bed'
    report_bed_sorted = open(report_bed_sorted_filepath, 'w')
    report_bed_sorted.write(results_sorted)
    report_bed_sorted.close()
    os.remove(report_bed_filepath)


# extract list of unique variants that intersect both sorted bed file
# and panel bed file
def intersect(report_path):
    report_bed = report_path + 'report_bed_sorted.bed'
    intersect_command = (BEDTOOLS_FILEPATH + 'intersectBed -a ' + report_bed
        + ' -b ' + bedtools_input)
    try:
        results_intersect = os.popen(intersect_command).read()
    except IOError:
        print("error")
    results_intersect = [
        result for result 
        in results_intersect.split('\n') if result.strip() != ''
        ]
    results_intersect_unique = []
    for field in results_intersect:
        if field.split('\t')[3] not in results_intersect_unique:
            results_intersect_unique += [field.split('\t')[3]]
    os.remove(report_bed)
    return(results_intersect_unique)


def apply_panel(report_input, panel_name, intersect):
    # loop through the report, compare each variant to intersect list
    # and keep if they match
    header = (
        '#Panel applied: ' + str(panel_name) + '. Date: ' 
        + str(datetime.date.today()))
    header_list = [[header]]
    output_list = []
    with open(report_input) as report:
        results = csv.reader(report, delimiter='\t')
        for line in results:
            if line[0][0] == '#':
                header_list += [line]
            if line[0][0] != '#':
                if line[2] in intersect:
                    output_list += [line]
    # open file to save output
    panel_applied_filepath = (
        report_input.split('.')[0] + '_' + panel_name + '.txt'
    )
    panel_applied_output = open(panel_applied_filepath, 'w')
    # write header and then output to file
    wr = csv.writer(panel_applied_output, delimiter='\t')
    for row in header_list:
        wr.writerow(row)
    for row in output_list:
        wr.writerow(row)
    panel_applied_output.close()
    print('Output:      ' + panel_applied_filepath)


def filter_denovo(report_input):
    # loop through the report, add variant if workflow is de novo
    header = (
        '#Filtered: DE NOVO calls only. Date: ' + str(datetime.datetime.now())
    )
    header_list = [[header]]
    output_list = []
    with open(report_input) as report:
        results = csv.reader(report, delimiter='\t')
        for line in results:
            if line[0][0] == '#':
                header_list += [line]
            if line[0][0] != '#':
                if 'DE_NOVO' in line[1]:
                    output_list += [line]
    # open file to save output
    panel_applied_filepath = report_input.split('.')[0] + '_DE_NOVO.txt'
    panel_applied_output = open(panel_applied_filepath, 'w')
    # write header and then output to file
    wr = csv.writer(panel_applied_output, delimiter='\t')
    for row in header_list:
        wr.writerow(row)
    for row in output_list:
        wr.writerow(row)
    panel_applied_output.close()
    print('Output:      ' + panel_applied_filepath)


# CALL FUNCTIONS -------------------------------------------------------------
print('Applying panels...\n')
(report_input, panel_input, bedtools_input, report_path, 
    panel_name) = load_variables()
make_report_bed(report_input, report_path)
results_intersect_unique = intersect(report_path)
apply_panel(report_input, panel_name, results_intersect_unique)
filter_denovo(report_input)
print('\nDone.')
