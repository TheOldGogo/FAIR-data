#20241230 - JG - tentatively adding an automatic detection of a date and its conversion to ISO-8601 format

import pandas as pd
import yaml
import pytz

def update_yaml_with_excel_data(excel_file_path, yaml_file_path, sheet_name, target_columns, destination_fields):

    # Read the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    # Read the existing YAML file
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # Process each field path and target column pair
    for destination_field, target_column in zip(destination_fields, target_columns):
                                      
        # Get the first cell of the specified column
        first_cell = df[target_column].iloc[0]

        # if the required field is a date: convert it to ISO-8601 format
        if ' date' in target_column:
            dated_cell = pd.to_datetime(first_cell, format='%d/%m/%Y')
            timezone = pytz.timezone("Asia/Riyadh") # may want to put that higher at some point
            datetime_with_tz = timezone.localize(dated_cell)
            first_cell = datetime_with_tz.strftime('%Y-%m-%dT%H:%M:%S%z')


        # Split the field path into individual components
        path_components = destination_field.split('>')

        # Navigate through the YAML structure
        current = yaml_data
        for component in path_components[:-1]:
            if component not in current:
                current[component] = {}
            current = current[component]

        # Update the last component with the new data
        if path_components[-1] in current:
            current[path_components[-1]] = first_cell
        else:
            print(f"Warning: {path_components[-1]} not found in the YAML file.")


    # Write the updated YAML back to a file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file)

#update_yaml_with_excel_data('.\Additional information.xlsx', '.\eln_Jules_D18_vms_KSC_UPS - try autofill.yaml','Materials',['Usual name','CAS ID','CAS name', 'Hill Molecule Formula','CAS synonyms'], ['sample>substance>name','sample>substance>cas_number','sample>substance>cas_name','sample>substance>molecular_formula_hill','sample>substance>cas_synonyms'])