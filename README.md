# Apply panels to trio analysis output

The VariantReporterSpark trio analysis pipeline produces a txt file output containing a list of variants with no panel applied. This script takes one or more panels and applies them to the trio variant report output.

## Requirements  

- Python 2.7.8 (the scripts should run with Python 3 but this hasn't been tested)
- virtualenv (or venv with python 3)
- pybiomart (version 0.2.0)
- pandas (version 0.23.3)

### Setup

- Make new directory called trio_analysis
- Clone this repo into the new directory
- Make folders to save BED files
- Setup a virtual environemnt within this directory, install pandas and pybiomart  

In Python 2:
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
  |-- validated_bed_files         Validated BED files.
  |-- trio_env                    Virtual environment.
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

- Run the script to create the panel. PanelApp ID can be found on the PanelApp website.  
```python query_panelapp.py <PanelApp_ID>```  

- This will save a BED file of the selected panel within the ```panelapp_bed_files``` folder

- Once this BED file has been checked, move it into the ```validated_bed_files``` folder

- Deactivate virtual environment  
```deactivate```  

## Applying a panel to the trio variant report  

- If not already active, activate the virtual environment  
Within the trio_analysis folder: ```source trio_env/bin/activate```  

- Apply panel(s) to trio variant report  
```python apply_panel_trios.py <path_to_variant_report> <path_to_BED_file> [OPTIONAL: <path_to_more_BED_files>]```  

- This will output two folders in the same results folder as the original trio variant report - ```<trio_variant_report>_<panel_name>.txt``` and ```<trio_variant_report>_DE_NOVO.txt```

- Deactivate virtual environment  
```deactivate```  
