#from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
#from neurospeed.utils.helper_service import UtilService

from neurospeed.hia_user_data.neurobrave_sensor_interface import HIA_Client

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.api_http_handlers.recorder_http_handler import UserRoom_Recorder_Handler
from neurospeed.api_http_handlers.exporter_http_handler import UserRoom_Recorder_Exporter_Handler
from neurospeed.api_http_handlers.insight_http_handler import Insight_User_Handler
from neurospeed.api_http_handlers.customer_account_manager import Customer_Account_Manager
from neurospeed.utils.helper_service import UtilService
from neurospeed.api_http_handlers.customer_account_manager import Customer_Account_Manager

import json
import numpy as np
import time 
import logging
import requests
from datetime import datetime
import os
from dateutil import tz
import pytz
from neurospeed.constants import PROD_API_CONFIG



def find_running_recorder(customer_auth, username, api_config = PROD_API_CONFIG):
    recorder_handler = UserRoom_Recorder_Handler(customer_auth, api_config=api_config)
    list_recorders = recorder_handler.list_recorders(1, 50, {"username": username})
        
    if list_recorders is not None:
        for index, item in enumerate(list_recorders["pager"]["items"]):
            if not list_recorders["pager"]["items"][index]["status"] == "stopped":
                logging.debug("discovered Recorder with status not stopped, stopping recorder")                
                rec_id = list_recorders["pager"]["items"][index]["id"]                
                return rec_id
    return None

def run_recorder_flow(recorder_handler, hia_config, recorder_name = "default"):
    '''
    create data recorder instance on cloud.
    recorder created with status "resource_pending".
    once available recording resources found and assgined
    recorder status will change to "pending",
    then once recorder picked by assigned recorder resources and start to record status will change to "recording"
    '''
     
    username = hia_config["username"]
    # set up data recorder instance:
    # list_recorders = recorder_handler.list_recorders(0,50)
    
    list_recorders = recorder_handler.list_recorders(1, 50, {"username": username})
    logging.debug("list of existing recorders:")
    if type(list_recorders) == dict:
        logging.debug(list_recorders.keys())
    if list_recorders is not None:
        for index, item in enumerate(list_recorders["pager"]["items"]):
            if not list_recorders["pager"]["items"][index]["status"] == "stopped":
                logging.debug("discovered Recorder with status not stopped, stopping recorder")                
                rec_id = list_recorders["pager"]["items"][index]["id"]
                recorder_handler.update_recorder(rec_id, "stopped")                 
                while True:                    
                    if recorder_handler.get_recorder(rec_id)["status"] == "stopped":
                        logging.debug("stopped recorder successfully")
                        time.sleep(5)
                        break


    recorder = recorder_handler.create_recorder(username = username, recorder_name = recorder_name)
    if recorder == None:
        logging.debug("failed to create recorder")
        return None
        
    recorder_id = str(recorder["id"])
    logging.debug('created recorder with id' + recorder_id)
    # get recorder ID for further administration:
    recorder = recorder_handler.get_recorder(recorder_id)     
    logging.debug("recorder status: " + recorder["status"])
    
    # wait until cloud resources allocated to recorder:
    recorder_recording = False
    max_query_attemps = 5
    query_attemps = 1
    while (recorder_recording != True & (query_attemps < max_query_attemps) ):
        recorder = recorder_handler.get_recorder(recorder_id)   
        logging.debug("recorder status: " + recorder["status"])
        if (recorder["status"] == "recording"):
            logging.debug('recorder started recording')
            recorder_recording = True
        else:
            logging.debug('recorder not recording yet')
            query_attemps = query_attemps + 1
            time.sleep(10)
             
    if (recorder_recording != True):
        logging.debug('recorder not yet recording after ' + str(query_attemps)  + ' query attempts')
        recorder_handler.delete_recorder(recorder_id)
        return None
     

    # #once recorder starts recording, you can change it's status to paused or stopped. you can resume paused recorder but not stopped recorder
    # # pause recorder:
    # res = recorder_handler.update_recorder(recorder_id, "paused")
    # recorder = recorder_handler.get_recorder(recorder_id)     
    # print("recorder status: " + recorder["status"])
    # time.sleep(15)
    
    # # reactivate paused recorder
    # recorder_handler.update_recorder(recorder_id, "pending") 
    # recorder = recorder_handler.get_recorder(recorder_id)     
    # print("recorder status: " + recorder["status"])
 
    #recorder_handler.delete_recorder(recorder_id) # uncomment this to delete recorder
    # recorders = recorder_handler.list_recorders(username)
    # print(recorders)
    
     
    
    
    return recorder_id


def start_recording(customer_auth, hia_config, recorder_name, api_config = PROD_API_CONFIG):
    recorder_handler = UserRoom_Recorder_Handler(customer_auth, api_config=api_config)   
    recorder_id = run_recorder_flow(recorder_handler, hia_config, recorder_name)
    
    while recorder_id is None:
        print("FAILED starting the cloud recording serivce! Retrying.\n")
        recorder_id = run_recorder_flow(customer_auth, hia_config, recorder_name)
    return recorder_id


def get_user_insights(customer_auth,username, api_config = PROD_API_CONFIG):
    insight_handler = Insight_User_Handler(customer_auth, api_config)
    cam = Customer_Account_Manager(customer_auth, api_config)
    user_id = cam.get_user_id(username)
    insights = insight_handler.get_user_insights(user_id)
    return insights


def get_user_alltime_insights(customer_auth,username,start_date,end_date,insight_type="output$neurobrave_stress2",boundry="hour", api_config = PROD_API_CONFIG):
    insight_handler = Insight_User_Handler(customer_auth, api_config)
    cam = Customer_Account_Manager(customer_auth, api_config)
    user_id = cam.get_user_id(username)
    
    insights = insight_handler.get_user_alltime_insights(user_id,start_date,end_date,insight_type,boundry)
    return insights


def get_user_insights_stats(customer_auth,username,daily_date,insight_type="output$neurobrave_stress2",boundry="day", api_config = PROD_API_CONFIG):
    """
    The function will return the statistics for date_day_day only.
    boundry can be day/week/month.
    """
    insight_handler = Insight_User_Handler(customer_auth, api_config)
    cam = Customer_Account_Manager(customer_auth, api_config)
    user_id = cam.get_user_id(username)
    insights = insight_handler.get_user_insights_stats(user_id,daily_date,insight_type,boundry)
    
    return insights

def get_user_all_insights_stats(customer_auth,username,daily_date,insight_type="output$neurobrave_stress2",boundry="day", api_config = PROD_API_CONFIG):
    """
    The function will return the statistics of all dates up to and including daily_date
    boundry can be hour/day/week/month.
    """
    insight_handler = Insight_User_Handler(customer_auth, api_config)
    cam = Customer_Account_Manager(customer_auth, api_config)
    user_id = cam.get_user_id(username)
    
    insights = insight_handler.get_user_all_insights_stats(user_id,daily_date,insight_type, boundry)
    return insights

def get_user_stress_baseline(auth, username = None, api_config = PROD_API_CONFIG, insight_type="output$neurobrave_stress2"):
    """
    The function will return the daily stress
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_user_stress_baseline(insight_type, user_id)
    else:
        insights = insight_handler.get_user_stress_baseline(insight_type)
    
    return insights

def get_user_daily_stress(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the daily stress
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_user_daily_stress(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_user_daily_stress(daily_date, timezone)
    
    return insights

def get_user_battery(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the daily stress
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_user_battery(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_user_battery(daily_date, timezone)
    
    return insights

def get_user_hourly_insights(auth, daily_date,timezone = None, username = None, api_config = PROD_API_CONFIG):
    insight_handler = Insight_User_Handler(auth, api_config)
    
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_user_hourly_insights(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_user_hourly_insights(daily_date, timezone)
    
    return insights

def get_user_history_hourly_insights(auth, timezone = None, username = None, api_config = PROD_API_CONFIG):
    insight_handler = Insight_User_Handler(auth, api_config)
    
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_user_history_hourly_insights(timezone, user_id)
    else:
        insights = insight_handler.get_user_history_hourly_insights(timezone)
        
    return insights

def get_weekly_stress_average(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the weekly stress average
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_stress_average(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_weekly_stress_average(daily_date, timezone)
    
    return insights

def get_weekly_stress_change(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the weekly stress change
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_stress_change(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_weekly_stress_change(daily_date, timezone)
    
    return insights

def get_weekly_stress_index(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the weekly stress index
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_stress_index(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_weekly_stress_index(daily_date, timezone)
    
    return insights
    
def get_weekly_best_sleep(auth, daily_date, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the night and the value of the best sleep
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_best_sleep(daily_date, user_id)
    else:
        insights = insight_handler.get_weekly_best_sleep(daily_date)
    
    return insights

def get_weekly_worst_sleep(auth, daily_date, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the night and the value of the best sleep
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_worst_sleep(daily_date, user_id)
    else:
        insights = insight_handler.get_weekly_worst_sleep(daily_date)
    
    return insights
       
def get_weekly_stressful_time(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the most stressful time in the week
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_stressful_time(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_weekly_stressful_time(daily_date, timezone)
    
    return insights    

def get_weekly_quiet_time(auth, daily_date, timezone = None, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the most stressful time in the week
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_weekly_quiet_time(daily_date, timezone, user_id)
    else:
        insights = insight_handler.get_weekly_quiet_time(daily_date, timezone)
    
    return insights    
    
def get_first_day_of_the_week(auth, username = None, api_config = PROD_API_CONFIG):
    """
    The function will return the first day of users week.
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.get_first_day_of_the_week(user_id)
    else:
        insights = insight_handler.get_first_day_of_the_week()
    
    return insights  

def set_first_day_of_the_week(auth, first_day_of_week, username = None, api_config = PROD_API_CONFIG):
    """
    The function will update the first day of users week.
    """
    insight_handler = Insight_User_Handler(auth, api_config)
    if type(auth) == Auth_AS_Customer_handler:
        cam = Customer_Account_Manager(auth, api_config)
        user_id = cam.get_user_id(username)
        insights = insight_handler.set_first_day_of_the_week(first_day_of_week, user_id)
    else:
        insights = insight_handler.set_first_day_of_the_week(first_day_of_week, )
    
    return insights  
    
def delete_recording(customer_auth, recorder_id, api_config = PROD_API_CONFIG):
    recorder_handler = UserRoom_Recorder_Handler(customer_auth, api_config=api_config)
    recorder_handler.delete_recorder(recorder_id) 
    print("recorder status: " + recorder_handler.get_recorder(recorder_id)["status"])


def stop_recording(customer_auth, recorder_id, api_config = PROD_API_CONFIG):
    recorder_handler = UserRoom_Recorder_Handler(customer_auth, api_config=api_config)
    recorder_handler.update_recorder(recorder_id, "stopped") 
    print("recorder status: " + recorder_handler.get_recorder(recorder_id)["status"])


def run_exporter_flow(exporter_handler, recorder_id, exporter_config, hia_config, save_folder, max_query_attemps = 600):
    '''
    inputs:
        recorder id - string with recorder id in neurospeed that's used in this section
        exporter_config - dictionry with exported configuration. exporter name, time limits, fields to export.
        hia_config - dictionary with hia_config. used for the credentials.
        save_folder - absolute folder path to save the .csv file
    
    outputs:
        full absolute path to downloaded .csv file with data
        
        
    this function operates the exported on neurospeed via the neurospeed API.
    it runs exporter on cloud, waits for it to complete, and downloads the file using received temporary URL. 
    the URL deprecated quickly so don't expect it to work after even few minutes of completing the export. 
    
    the downloaded file is .csv, same format like downlaoding from exporter via neurospeed dashboard
    
    '''
    
    
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
        
    # create exporter, if recorder has no data, request will fail.
    exporter = exporter_handler.create_exporter(int(recorder_id), exporter_config)
    exporter_id = str(exporter["id"])

    exporter = exporter_handler.get_exporter(exporter_id)  
    logging.debug("EXPORTER: ")
    logging.debug(exporter)

    # once exporter created, query it's status until it "exported".
    for query_attempt in range(max_query_attemps):
        exporter = exporter_handler.get_exporter(exporter_id)  
        logging.debug("exporter status: " + exporter["status"])
        if (exporter["status"] == "exported"):
            logging.debug('exporter finished exporting')
            break
        time.sleep(2)
             
        
    if exporter["status"] != "exported":
        logging.debug('exporter not yet exported the file after  ' + str(max_query_attemps)  + ' query attempts')
        exporter_handler.delete_exporter(exporter_id)
        return None
   
    # once exporter exported the file, you can ask for an URL to download the exported file. 
    #the url available for only short time before it deprecates
    #get_exported_url(exporter_id) returns dictionary of structure {"url": "https://neurospeed...... ...."}
    url_response = exporter_handler.get_exported_url(exporter_id)["url"]  
    #delete_exporter(exporter_id) # uncomment this to delete exporter
    # list all exporters under username
    # exporters = exporter_handler.list_exporters(hia_config["username"])
    # print(exporters)    
    logging.debug("data download link: " + url_response)
    
    exported_filename = None
    try:
        print("downloading data from server, ignoring TLS certificate")
        exported_data = requests.get(url_response, verify = False)
        exported_filename = save_folder + "/_" + exporter_config["custom_name"] + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + '.csv'
        logging.debug("saving data to local file at " + exported_filename)
        with open(exported_filename, "wb")as f:
            f.write(exported_data.content)
    except Exception as e:
        logging.debug("failed to download the datafile, please attempt manual downlaod from the web dashboard")
        logging.debug(e)
    return exported_filename
    
    
def download_data(customer_auth, recorder_id, exporter_config, hia_config, save_folder, max_query_attemps = 600, api_config = PROD_API_CONFIG):
    
    '''
    this function tries to download the CSV datafile from neurospeed cloud,
    the download will fail in case of non-exsiting recording or in case that donwloads from AWS cloud are blocked by the network
    
    returns full absolute path to the downloaded data file on local computer
    
    '''
    exporter_handler = UserRoom_Recorder_Exporter_Handler(customer_auth, api_config=api_config)
    exported_filename = run_exporter_flow(exporter_handler, recorder_id, exporter_config, hia_config, save_folder, max_query_attemps)
    return exported_filename


def get_all_existing_users(customer_auth, page_number = 1, page_size = 50, api_config = PROD_API_CONFIG):
    '''
    This function returns a list of all existing users associated with a customer account.
    
    Parameters:
    customer_auth (object): An authentication object that provides access to the customer account.
    
    Returns:
    list: A list of all existing users associated with the customer account. Each user in the list contains
          relevant user information, as provided by the `get_all_existing_users` method of `Customer_Account_Manager`.
    
    '''
    # Get the list of all existing users
    customer_account = Customer_Account_Manager(customer_auth, api_config=api_config)
    existing_users = customer_account.get_all_existing_users(page_number, page_size)
    return existing_users["pager"]["items"]


def generate_sensor_info(config, hia_config, use_local_timestamp = False):
    '''
    this functiuon generates sensor_info dictionary that is nesessary ot initialize the HIA client.
    the sensor info is tailored for single EEG according to config
    only LSL interface supported currently

    input:
        hia_config dictionary
    '''
    # generate SOME sensors stream ids
    sensor_info = dict()

    if "EEG" in config["DATA_SOURCE"]:
        user_data_stream_id = "EEG" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "EEG",
            "channel_count": len(hia_config["EEG_channel_enable"]),
            "sampling_frequency": hia_config["EEG_sample_rate"],
            "buffer_length": hia_config["EEG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["channel_map"]
        }
        
        if use_local_timestamp: 
            sensor_info[user_data_stream_id]["channel_map"] += ["timestamp"]
            

    if "PPG" in config["DATA_SOURCE"]:
        user_data_stream_id = "PPG" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "PPG",
            "channel_count": len(hia_config["PPG_channel_map"]),
            "sampling_frequency": hia_config["PPG_sample_rate"],
            "buffer_length": hia_config["PPG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["PPG_channel_map"]
        }
        if use_local_timestamp: 
            sensor_info[user_data_stream_id]["channel_map"] += ["timestamp"]

    if "SMARTWATCH" in config["DATA_SOURCE"]:
        user_data_stream_id = "SMARTWATCH" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "SMARTWATCH",
            "channel_count": len(hia_config["PPG_channel_map"]),
            "sampling_frequency": hia_config["PPG_sample_rate"],
            "buffer_length": hia_config["PPG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["PPG_channel_map"]
        }
        if use_local_timestamp: 
            sensor_info[user_data_stream_id]["channel_map"] += ["timestamp"]


    if "GSR" in config["DATA_SOURCE"]:
        for idx, port in enumerate(config["OPENBCI_COM_PORT"]):
            user_data_stream_id = "GSR" + '_' + UtilService.generateId(6)
            sensor_info[user_data_stream_id] = {"device_type": "GSR",
                                                "sensor_id": user_data_stream_id,
                                                "stream_id": user_data_stream_id,
                                                "sampling_frequency": 250,
                                                "buffer_length": 1.0,
                                                "manufacturer_id": "openBCI",
                                                "channel_count": len(config["GSR_channel_enable"][idx]),
                                                # "Downstream ID":downstream_id,
                                                "channel_map": config["GSR_channel_map"][idx],
                                                "stream_state": "enabled"}
            
            if use_local_timestamp: 
                sensor_info[user_data_stream_id]["channel_map"] += ["timestamp"]

    if "EDA" in config["DATA_SOURCE"]:
        user_data_stream_id = "GSR_ADIEDA"

        sensor_info[user_data_stream_id] = {"device_type": "GSR",
                                            "sensor_id": user_data_stream_id,
                                            "stream_id": user_data_stream_id,
                                            "sampling_frequency": config["EDA_sampling_frequency"],
                                            "buffer_length": 1.0,
                                            "manufacturer_id": "ADI",
                                            "channel_count": 6,
                                            # "Downstream ID":downstream_id,
                                            "channel_map": ['real', 'img', 'adm_real', 'adm_img', 'adm_mag',
                                                            'adm_phase', "timestamp"],
                                            "stream_state": "enabled"}
        if use_local_timestamp: 
            sensor_info[user_data_stream_id]["channel_map"] += ["timestamp"]
         
            
    logging.debug(f"generated sensor info {sensor_info}")
    return sensor_info


def init_HIA_client(config, hia_config, use_local_timestamp = False, api_config=PROD_API_CONFIG):
    '''
    this functiuon  initialize the HIA client and connect the cloud streaming (upload raw data to neurospeed)
    the sensor info is tailored for single EEG according to config
    only LSL interface supported currently

    input:
        config - dictionary with config for this epxeriment program
        hia_config dictionary

    output
        hia_user client object instance
        sensor info dictionary

    '''
    retries=3
    for _ in range(retries):
        try:
            user1_auth = Auth_AS_User_Handler(hia_config)
            user1_auth.login()

            hia_sensor_info_user = generate_sensor_info(config, hia_config, use_local_timestamp)

            logging.debug('Generated sensor info: {}'.format(hia_sensor_info_user))
            hia_instance = HIA_Client(user1_auth, hia_sensor_info_user, api_config=api_config)
            
            #hia_user1.set_socket_connection_external_handler(connection_external_handler)
            # hia_user1.set_socket_disconnect_external_handler(disconnect_external_handler)  
            logging.debug("HIA_ID: " + str(user1_auth.get_hia_id()))
            hia_instance._device_type = "EEG"
            hia_instance.connect()
            break       
        except Exception as e:
            logging.debug(f"error while conneting HIA, retrying...: {e}")
            time.sleep(5)
    
    
    return hia_instance, hia_sensor_info_user


def get_stream_id_from_sensor_info(sensor_info, device_type = "EEG"):
    
    supported_devices = "EEG", "PPG", "SMARTWATCH", "GSR", "EDA", "USER_DATA"
    if device_type not in supported_devices:
        raise ValueError("device not supported")
    logging.debug(f"searching for {device_type} in local sensor_info..")
    stream_id = list(filter(lambda x: x.startswith(device_type), list(sensor_info.keys())))[0]
    logging.debug(f"found stream id {stream_id}")
    
    return stream_id


def send_datafile_to_neurospeed(data_array,timestamp_array = None, labels_array=None, Fs=256, channel_map = None, hia_config = None, window = None, device_type = "EEG",sleep_time=0.1):

    
    '''
    
    this function transmits data structure to neurospeed using HIA streaming, in realtime speed.
    inputs:
        data arry - a NUMPY data array of shape SAMPLES x CHANNELS
        timestamp  - NUMPY array of shape SAMPLEX X . 
        labels array - optional, numpy array of SAMPLES x 1 of strings that contain data lables
        Fs - data sampling frequency, 
        channel map - list of strings that specify channel names, must be same size as CHANNELS dimension of the data array
        hia_config- dictionary with neurospeed cloud user-level credentials - username, customer profile string, and the password
        window - optional, number of samples to send in each transmission packet
        
    '''
    
    
    
    if timestamp_array is None: 
        send_without_timestamp = True
        use_local_timestamp = False
    else: 
        send_without_timestamp = False
        use_local_timestamp = True
    
    
    hia_client = None
    
    if hia_config is None: 
        try:
            with open('config/hia_config.json') as f:
                hia_config = json.load(f)
        except:
            raise ValueError("unable to load HIA configuration file")
            
            
    device_type = device_type.upper()
    
    config = {}
    config["DATA_SOURCE"] = [device_type]  
    if window is None:
        EEG_buffer_length_seconds =  0.25
    else:
        EEG_buffer_length_seconds = window/Fs
    channel_count = np.min(data_array.shape)  
    if channel_map is None: 
        channel_map = [f"ch_{i}" for i in range(channel_count)]    
    hia_config["EEG_channel_enable"] = [i for i in range(channel_count)]
    hia_config["EEG_sample_rate"] = Fs
    hia_config["EEG_buffer_length_seconds"] = EEG_buffer_length_seconds 
    hia_config["channel_map"] = channel_map
   
    
    
    
    max_hia_reconnect_retries = 3
    for reconnect_idx in range(max_hia_reconnect_retries):
        try:
            hia_client, sensor_info = init_HIA_client(config, hia_config, use_local_timestamp)
        except Exception as e:
            logging.debug(f"exception while initializing HIA instance: {e}")
            time.sleep(3)
            continue
        if hia_client.is_connected():
            break
        else:
            logging.debug("HIA connection retrying...")
            time.sleep(3)

    if not hia_client.is_connected():
        raise ValueError("FAILED connecting to cloud streaming!\n")
        

    print("hia connection status: " + str(hia_client.is_connected()))
    
    
    
    sleep_time =sleep_time  #sleep time between packets, [seconds]
    
    
    stream_id = get_stream_id_from_sensor_info(sensor_info, device_type = device_type)
    if window is None:
        window = int(EEG_buffer_length_seconds * Fs) 
            
    if labels_array is not None:
        if not np.max(labels_array.shape) == np.max(data_array.shape):
            raise ValueError("data and event array length mismatch!")
    
    read_index = 0
    current_label = None
    #print(f"length of data: {len(data_array)}")
    print(f"shape of the array is {data_array.shape}")
    print("tranmsmitting data packets...")
    while read_index + window < len(data_array):
        data = data_array[read_index:read_index + window, :].tolist()
        timestamp = timestamp_array[read_index:read_index + window].tolist()
        #print(f"data: {type(data)}, {data}")
        read_index += window
        hia_client.send_data_direct(data, stream_id = stream_id, timestamp = timestamp, send_without_timestamp=send_without_timestamp, device_type=device_type)
        print(".", end="")
        
        time.sleep(sleep_time)
        
        if labels_array is not None:
            if labels_array[read_index] != current_label:
                hia_client.set_label(str(labels_array[read_index]))
                current_label = labels_array[read_index]
                print("")
                print(f"setting label to {current_label}")


    hia_client.disconnect()
    time.sleep(1)
    if hia_client.is_connected():
        print("HIA connection status: CONNECTED")
    else:
        print("HIA connection status: DISCONNECTED")
    

def is_exporter_datafile(file):
    #this function receives ABSOLUTE PATH to data file, and checks if the file is 
    #in fact a datafile produced by NeuroSpeed cloud recorder. 
    min_size = 1E4
    if not ".csv" in file:
        return False
    if  os.path.getsize(file) < min_size: 
        return False
    #read header only: 
    try:
        header = np.loadtxt(file, delimiter=",", max_rows=1, dtype="str").tolist()
    except:
        return False
    if not "timestamp" in header:
        return False
    if not "packets_counter" in header:
        return False
    if not "stream_id" in header:
        return False
    if not "device_type" in header:
        return False

    return True  


def find_exporter_files(folder):
    # print(f"checking {folder}")
    list_of_files=[]
    for item in os.listdir(folder):   
        if is_exporter_datafile(os.path.join(folder, item)):
            list_of_files.append(os.path.join(folder, item))
            # print(f"discovered {os.path.join(workdir, item)}")
        if os.path.isdir(os.path.join(folder, item)):
            # print(f"recursing into {os.path.join(folder, item)}")
            list_of_files+=find_exporter_files(os.path.join(folder, item))
    return list_of_files

