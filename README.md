# Apply panels to trio analysis output

The VariantReporterSpark trio analysis pipeline produces a txt file output containing a list of variants with no panel applied. This script takes one or more panels and applies them to the trio variant report output.

## Requirements  

- Python 2.7.8 (the scripts should run with Python 3 but this hasn't been tested)
- virtualenv (or venv with python 3)
- pybiomart (v )
- pandas (v )

### Setup

- Make new directory called trio_analysis
- Clone this repo into the new directory
- Make folders to save BED files
- Setup a virtual environemnt within this directory, install pandas and pybiomart
```
virtualenv <path_to_trio_folder>/trio_analysis/trio_env
pip install pandas
pip install pybiomart
```
- Change variables in capitals at top of each script before running
    - ```BEDTOOLS_FILEPATH``` - path to bin folder of BEDTools installation
    - ```GENOME_FILEPATH``` - path to hg19.genome file
    - ```OUTPUT_LOCATION``` - path to panelapp_bed_files folder

### Files

After setup the trio_analysis folder should look this this:  

```
trio_analysis
  |-- trio_env                    Virtual environment.
  |-- trio_bed_files              Validated BED files.
  |-- panelapp_bed_files          Output location for panelApp BED files.
  |-- query_panelapp.py           From this repo.
  |-- hg19.genome                 For BEDTools slop. From this repo.
  |-- apply_panel_trios.py        From this repo.
  |-- .pybiomart.sqlite           Made during pybiomart installation.
```

## Creating a PanelApp BED file  

You can either apply your own panel to the trio variant report, or you can use this script to produce a BED file from a PanelApp panel.  

- Activate the virtual environment  
```source trio_env/bin/activate```  

- Create panel  
```python query_panelapp.py <PanelApp ID>```   

- Deactivate virtual environment  
```deactivate```  

## Applying a panel to the trio variant report  

- If not already active, activate the virtual environment  
Within the trio_analysis folder: ```source trio_env/bin/activate```  

- Apply panel(s) to trio variant report  
```python apply_panel_trios.py <path_to_variant_report> <path_to_BED_file> [OPTIONAL: <path_to_more_BED_files>]```  

- Deactivate virtual environment  
```deactivate```  
