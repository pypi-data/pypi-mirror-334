# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:34:45 2021

@author: NeuroBrave
"""


import socketio 
from neurospeed.utils.api_config_service import ApiConfig
from neurospeed.constants import PROD_API_CONFIG

class UserRoom_AS_User_Handler:    
    
    def __init__(self, user_auth_handler, api_config = PROD_API_CONFIG):
        self._user_auth = user_auth_handler
        self._user_access_token = self._user_auth.get_access_token()
        self._username = self._user_auth.get_username()
        self._data_external_handler = None
        self._event_external_handler = None
        
        # Create UserRoom_Api api instance 
        self._userRoom_api = self.UserRoom_Api(self._user_auth, api_config=api_config)


    def userRoom_socket_connection_handler(self):
         print("User {} connected to UserRoom".format( self._username ))
    
    def userRoom_socket_disconnect_handler(self):
        print("User {} disconnected from UserRoom".format(self._username ))
    
       
    
    # internal data handler for HIA output data from Neurospeed pipeline    
    def userRoom_data_handler(self, payload):
        stream_id = payload["stream_id"]
        device_type = payload["device_type"]
        hia_id = payload["hia_id"]
        sensor_info = payload["sensor_info"]

        # propogate data to main program (or to any other source, depends on the external_handler callback)
        if (self._data_external_handler != None):
            self._data_external_handler(payload)
            
            
    # receive live events like hia connect\disconnect for this specific user    
    def userRoom_events_handler(self, payload): 
        
         # propogate event to main program (or to any other source, depends on the external_handler callback)
        if (self._events_external_handler != None):
            self._events_external_handler(payload)

        
    def set_data_external_handler(self, handler):
       self._data_external_handler = handler
   
    def set_device_events_external_handler(self, handler):
       self._events_external_handler = handler   



    def connect(self):
        # attach relevant handlers for socket.io events
        self._userRoom_api.set_connection_handler(self.userRoom_socket_connection_handler)
        self._userRoom_api.set_disconnect_handler(self.userRoom_socket_disconnect_handler)
        self._userRoom_api.set_data_handler(self.userRoom_data_handler)
        self._userRoom_api.set_events_handler(self.userRoom_events_handler)
        
        # connect 
        self._userRoom_api.connect()
        
    def disconnect(self):
        self._userRoom_api.disconnect()
            
    def get_username(self):
        return self._username


    class UserRoom_Api:    
        
        def __init__(self, config, api_config =PROD_API_CONFIG):
            api_config = ApiConfig(api_config)
            self._socket_url = api_config.get_socket_url()
            
            self._config = config
            self._user_access_token = self._config.get_access_token()
            self._username = self._config.get_username()
            
            logger_on = True
            if self._config.is_verbose_log() == False:
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
                "jwt_token": self._user_access_token,  
            }
         
            print("UserRoom_Api - Connecting to {} UserRoom as USER ".format(self._username))
            self._sio.connect(url = self._socket_url, transports ='websocket', headers=headers, socketio_path= '/target_is_user_room_as_user' ) 
    
        def disconnect(self):
           self._sio.disconnect()