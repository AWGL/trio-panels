# Apply panels to trio analysis output

## 1. Introduction

The VariantReporterSpark trio analysis pipeline produces a text file output containing a list of variants (and annotations) without any panels applied.
The clinical scientist has to apply a virtual panel to the report and analyse all variant calls within this panel.
The panel applied depends on the phenotype of the patient and most of the time it will be taken from PanelApp (https://panelapp.genomicsengland.co.uk).

Additionally, all *de novo* calls are anlaysed, regardless of whether they are within a panel or not.

This repository contains two scripts:

- `query_panelapp.py`: This script takes a PanelApp ID and makes a BED file of the genes within that panel

- `apply_panel_trios.py`: This script takes one or more panels and applies them to the trio variant report output. It also outputs a seperate file containing all *de novo* calls

---

## 2. Setup

### Requirements  

- Python 2.7.8 (the scripts should run with Python 3 but this hasn't been tested)
- virtualenv (or venv with python 3)
- pybiomart (version 0.2.0)
- pandas (version 0.23.3)

### Setup instructions

- Clone this reposirory into the new directory called trio_analysis
- Make folders to save BED files:
  - `panelapp_bed_files`: Output location for panelApp BED files from the `query_panelapp.py` program. 
  This is saved in the temp folder because it is a mapped drive that can be accessed from normal workstations. 
  - `validated_bed_files`: Bioinformatics department move BED files from `panelapp_bed_files` to here after they've been checked by a clinical scientist.
- Setup a virtual environment within this directory, install pandas and pybiomart  

In Python 2:

```
virtualenv <path_to_trio_folder>/trio_analysis/trio_env
pip install pandas
pip install pybiomart
```

- Change variables in capitals at top of each script before running
  - `BEDTOOLS_FILEPATH` - path to bin folder of BEDTools installation
  - `GENOME_FILEPATH` - path to hg19.genome file (required for BEDTools slop)
  - `OUTPUT_LOCATION` - path to panelapp_bed_files folder

### Files

After setup the trio_analysis folder should look this this:  

```
trio_analysis/
  |-- validated_bed_files/        Validated BED files.
  |-- trio_env/                   Generated with the virtual environment.
  |-- query_panelapp.py           From this repo.
  |-- hg19.genome                 Gives the size of each chromosome, required for BEDTools slop. From this repo.
  |-- apply_panel_trios.py        From this repo.
  |-- .pybiomart.sqlite           Generated during pybiomart installation.

temp/
  |-- panelapp_bed_files/         Output location for panelApp BED files.
```

---

## 3. SOP

- Once the clinical scientist/ clinician has decided the panel(s) that they will apply, they will email the bioinformatics department requesting that the panel is applied to the report.

- If you need to make a BED file from PanelApp, see **Section 5. Creating a PanelApp BED file** before continuing.

> **NOTE: Second checking BED files.** All new BED files must be double checked by a scientist before being used for reporting, see Section 5 for details.

- If you have the necessary BED files, follow the instructions in the **Section 4. Applying a panel to the trio variant report** section to apply the panel.

- Once the script has run, let the scientist know that the results are ready.

---

## 4. Applying a panel to the trio variant report  

This script applies one or more BED file to the trio analysis variant report.  
The BED file can be either a PanelApp BED file made in the step below, or any other BED file. 

More than one BED file can be inputted, just add each file as an optional extra input.  

### Instructions for running the script

- If not already active, activate the virtual environment: `source trio_env/bin/activate`

- Apply panel(s) to trio variant report. 

`python apply_panel_trios.py <path_to_variant_report> <path_to_BED_file> [OPTIONAL: <path_to_more_BED_files>]`

- This will output two files in the same results folder as the original trio variant report:
  - `<trio_variant_report>_<panel_name(s)>.txt` - The variant calls in the report that fall within the selected BED file(s)
  - `<trio_variant_report>_DE_NOVO.txt` - All *de novo* variant calls (the scientists will look at all *de novo* calls, this part of the script ensures that they don't accidentally see any other results while filtering the original file.)

- Deactivate virtual environment: `deactivate`

---

## 5. Creating a PanelApp BED file  

This script takes a PanelAppID and queries the PanelApp and BioMart APIs produce a BED file from a PanelApp panel.  
If you do not need to make a new BED file from PanelApp you can skip to the next section.  

By default, the output will contain only green genes and will have padding of 20 base pairs on either side of the intervals.
The code can easily be changed to change these settings.  

### Second checking new BED files

All new BED files must be double checked by a clinical scientist before being used for reporting. 
BED files are outputted into the `panelapp_bed_files` folder on  the temp drive.
This drive should be accessible from all workstations, if not then ask the bioinformatics department about getting the drive mapped.

Once the file has been checked, the clinical scientist should notify the bioinformatics department, who will copy the BED file into the `validated_bed_files` folder.
This folder is only accessible through the command line.

BED files in the `validated_bed_files` folder are ready to be used for analysis.

### Instructions for running the script

- Activate the virtual environment: `source trio_env/bin/activate`

- Run the script to create the panel. PanelApp ID can be found on the PanelApp website.  

`python query_panelapp.py <PanelApp_ID>`

- This will save a BED file of the selected panel within the `panelapp_bed_files` folder.

- Once this BED file has been checked, move it into the `validated_bed_files` folder.

- Deactivate virtual environment: `deactivate`
