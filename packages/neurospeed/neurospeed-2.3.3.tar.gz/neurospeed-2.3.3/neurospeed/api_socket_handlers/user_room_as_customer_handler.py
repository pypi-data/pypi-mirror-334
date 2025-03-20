# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:34:45 2021

@author: NeuroBrave
"""


import socketio 
from neurospeed.utils.api_config_service import ApiConfig
from neurospeed.constants import PROD_API_CONFIG

class UserRoom_AS_Customer_Handler:    
    
    def __init__(self, customer_auth_handler, username, api_config = PROD_API_CONFIG):
        self._customer_auth = customer_auth_handler
        self._customer_access_token = self._customer_auth.get_access_token()
        self._customer_email = self._customer_auth.get_customer_email()
        self._username = username
        self._data_external_handler = None
        self._events_external_handler = None
        
        # Create UserRoom_Api instance
        self._userRoom_api = self.UserRoom_Api(self._customer_auth, self._username, api_config=api_config)



    def userRoom_socket_connection_handler(self):
         print("Customer {} connected to user's {} UserRoom".format(self._customer_email, self._username ))
    
    def userRoom_socket_disconnect_handler(self):
        print("Customer {} disconnected from user's {} UserRoom".format(self._customer_email, self._username ))
    

    # internal data handler for HIA output data from Neurospeed pipeline    
    def userRoom_data_handler(self, payload):
        stream_id = payload["stream_id"]
        device_type = payload["device_type"]
        hia_id = payload["hia_id"]
        sensor_info = payload["sensor_info"]
        
        # propogate data to external handler if exist
        if (self._data_external_handler != None):
            self._data_external_handler(self, payload) # send current instance contex and payload
            
            
    # internal data handler for live events like hia connect\disconnect for specific user
    # see README(4) for payload structure  
    def userRoom_events_handler(self, payload): 
     
        # propogate data to external handler if exist
        if (self._events_external_handler != None):
            self._events_external_handler(self, payload) # send current instance contex and payload

 
    def set_data_external_handler(self, handler):
       self._data_external_handler = handler
   
    def set_events_external_handler(self, handler):
       self._events_external_handler = handler
       
       
    def connect(self):
        # attach relevant handlers for socket.io events
        self._userRoom_api.set_connection_handler(self.userRoom_socket_connection_handler)
        self._userRoom_api.set_disconnect_handler(self.userRoom_socket_disconnect_handler)
        self._userRoom_api.set_data_handler(self.userRoom_data_handler)
        self._userRoom_api.set_events_handler(self.userRoom_events_handler)
        
        self._userRoom_api.connect()
        
    def disconnect(self):
        self._userRoom_api.disconnect()
            
        
    def get_username(self):
        return self._username


    class UserRoom_Api:    
        
        def __init__(self, auth_handler, username, api_config = PROD_API_CONFIG):
            api_config = ApiConfig(api_config)
            
            self._auth_handler = auth_handler
            self._customer_access_token = self._auth_handler.get_access_token()
            self._username = username
            self._socket_url = api_config.get_socket_url()
            
            logger_on = True
            if self._auth_handler.is_verbose_log() == False:
                logger_on = False
                
            self._sio = socketio.Client(logger=logger_on, engineio_logger=False,  reconnection_delay  = 5, reconnection = True) 


        def set_connection_handler(self, handler):
            self._sio.on('connect',handler = handler)
            
        def set_disconnect_handler(self, handler):
            self._sio.on('disconnect', handler = handler)
            
        def set_data_handler(self, handler):
            self._sio.on('data', handler = handler)
         
        def set_events_handler(self, handler):
            self._sio.on('events', handler = handler)
            
    
        def connect(self):
            headers = {
                "jwt_token": self._customer_access_token,  # required
                "username": self._username, # required
            }
            print("UserRoom_Api - Connecting to user's {} UserRoom as CUSTOMER ".format(self._username))
            self._sio.connect(url = self._socket_url, transports ='websocket', headers=headers, socketio_path= '/target_is_user_room_as_customer' ) 
    
        def disconnect(self):
           self._sio.disconnect()