# JG: 2025-02-27: This is the alpha version of the GUI interface to FAIRize PES data and upload it to NOMAD
# it (should) works but there are critical missing functionalities 
# the development version can be found in the jupyter notebook test.ipynb

from pathlib import Path
import solara
from solara.website.utils import apidoc


# JG:2025-01-29: force reinstall nomad-API as for some reason it doesn't seem to be found
#!pip install nomad-api --force-reinstall


# Import your custom module

from ELNfiller import update_yaml_with_excel_data
from pynxtools.dataconverter.convert import convert

from Nomad_API import *



# class SharedState:
#     def __init__(self):
#         self.file = None
#         self.path = None

# shared_state = SharedState()

User_Excel_ELN = solara.reactive(None)
Setup_ELN = solara.reactive(None)
Data_file = solara.reactive(None)


@solara.component
def ELN_updater():
    
    User_Excel_ELN, set_file = solara.use_state(None)
    Setup_ELN, set_path = solara.use_state(None)
    directory, set_directory = solara.use_state(None)

    
    with solara.VBox() as main:
         can_select = solara.ui_checkbox("Enable select")

         def reset_path():
             set_path(None)
             set_file(None)

         #reset path and file when can_select changes
         solara.use_memo(reset_path, [can_select])
         solara.FileBrowser(directory, on_directory_change=set_directory, on_path_select=set_path, on_file_open=set_file, can_select=can_select)
         solara.Info(f"You are in directory: {directory}")
         solara.Info(f"Single click on the ELN: {Setup_ELN}")
         solara.Info(f"Double click on the XLS: {User_Excel_ELN}")

          #now trying to make something with those files
         def handle_button_click():
            update_yaml_with_excel_data(User_Excel_ELN, Setup_ELN,
                'Materials',['Usual name','CAS ID','CAS name', 
                'Hill Molecule Formula','CAS synonyms'], 
                ['sample>substance>name','sample>substance>cas_number',
                    'sample>substance>cas_name','sample>substance>molecular_formula_hill','sample>substance>cas_synonyms'])
            update_yaml_with_excel_data(User_Excel_ELN, Setup_ELN,
                'Sample preparation',['Sample preparation date','Sample preparation date','Sample preparation date','Sample preparation date'], 
                ['sample>history>sample_preparation>start_time','sample>history>sample_preparation>end_time','start_time','end_time'])


         solara.Button(label="Update ELN file", 
                        on_click = handle_button_click)
         
@solara.component
def Nexus_file_and_upload():
    
    Data_file, set_file = solara.use_state(None)
    Setup_ELN, set_path = solara.use_state(None)
    directory, set_directory = solara.use_state(None)

    
    with solara.VBox() as main:
         can_select = solara.ui_checkbox("Enable select")

         def reset_path():
             set_path(None)
             set_file(None)

         #reset path and file when can_select changes
         solara.use_memo(reset_path, [can_select])
         solara.FileBrowser(directory, on_directory_change=set_directory, on_path_select=set_path, on_file_open=set_file, can_select=can_select)
         solara.Info(f"You are in directory: {directory}")
         solara.Info(f"Double click on the DataFile: {Data_file}")
         
         Nexus_file_name = str(Data_file)[:-3] + 'nxs'


          #now trying to make something with those files
         def handle_button_click():
             #TODO: interface to prompt the File name 
             #2024-12-05: changed the filename to the datafile name + nxs extension
             convert([str(Data_file), str(Setup_ELN)], "xps", "NXmpes", Nexus_file_name, config_file = '.\Config\config_vms.json')
                    
         solara.Button(label="Generate NXS file", 
                        on_click = handle_button_click)
         
         def handle_button2_click():
             #TODO: interface to prompt the user later
             username = '******************'
             password = '***************'

             nomad_url = 'http://10.72.203.137/nomad-oasis/api/v1/'
             token = get_authentication_token(nomad_url, username, password)
             
             #TODO: prompt dataset and upload ID name
             dataset_id = create_dataset(nomad_url, token, 'Test_Dataset')
             upload_id = upload_to_NOMAD(nomad_url + 'uploads?file_name=' + Nexus_file_name, token, Nexus_file_name)


             last_status_message = check_upload_status(nomad_url, token, upload_id)
             print(last_status_message)

             metadata = {
                "metadata": {
                "upload_name": 'Test_Upload',
                "references": ["https://doi.org/xx.xxxx/x.xxxx"],
                "datasets": dataset_id,
                "embargo_length": 0,
                "coauthor0s": ["jules.bertrandie@kaust.edu.sa@affiliation.de"],
                "comment": 'This is a test upload...',
             },
             }
             response = edit_upload_metadata(nomad_url, token, upload_id, metadata)
            
             last_status_message = check_upload_status(nomad_url, token, upload_id)
             print(last_status_message)
         
             #I put the publishing command lines there, but 'm not sure we should use them yet so I just put them as commands
             # response = publish_upload(nomad_url, token, upload_id)
             # last_status_message = check_upload_status(nomad_url, token, upload_id)
             # print(last_status_message)





             
                    
         solara.Button(label="Upload_To_Nomad_Oasis", 
                        on_click = handle_button2_click)

@solara.component
def Page():
    with solara.Column():
        with solara.Columns([1, 1]):
            ELN_updater()
            Nexus_file_and_upload()

#__doc__ += apidoc(solara.FileBrowser.f)  # type: ignore


