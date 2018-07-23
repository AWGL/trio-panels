# Apply panels to trio analysis output

The VariantReporterSpark trio analysis pipeline produces a txt file output containing a list of variants with no panel applied. This script takes one or more panels and applies them to the trio variant report output.

## Requirements  

The scripts are designed to be run within a virtual environment with pandas and pybiomart installed.  
Works with python 2 or 3.  
Change variables in capitals at top of each script before running.  

- Activate the virtual environment  
```source trio_env/bin/activate```  

- Deactivate virtual environment  
```deactivate```  

## Creating a PanelApp BED file  

You can either apply your own panel to the trio variant report, or you can use this script to produce a BED file from a PanelApp panel.  

- Create panel  
```python query_panelapp.py <PanelApp ID>```   

## Applying a panel to the trio variant report  

- Apply panel(s) to trio variant report  
```python apply_panel_trios.py <path_to_variant_report> <path_to_BED_file> [OPTIONAL: <path_to_more_BED_files>]```  

