import core.connection
import core.globals
import random
import time

connection_description = 'Connection for simulating sensor data with random Number generator.'
connection_version = '0.01'
connection_author = 'Christian Kueken, Germany'

connection_parameters = {'frequency': 'Interval time. How often (in seconds) will a new number be generated.'}

connection_datapoint_parameters  = {'min': 'Minimal Output Number',
                                    'max': 'Minimal Output Number'}

class Random(core.connection.Connection):

    def __init__(self, name=None, friendly_name=None, interval=1.0):

        super().__init__(name, friendly_name, interval)                  # Init core.connection.Connection
        self.status = 'stopped'                                          # Set status to stopped to indicate the connection can start receiving


    def user_receive(self):
        min = 0.0
        max = 100.0

        # Iterate through all Datapoints
        for dp_key, dp_obj in core.globals.pool['data'].items():

            # Check if actual dp belongs to this connection object
            if dp_obj.conn == self:

                if 'min' in dp_obj.conn_para:       # Get Connection Parameters from dp safely by checking existence
                    min = dp_obj.conn_para['min']

                if 'max' in dp_obj.conn_para:
                    max = dp_obj.conn_para['max']

                dp_obj.setValue(random.uniform(min, max), RawValue=True, SetByConn=True)        # Set Random Raw Value

                # Connections in general should only receive and set raw Values. The value for displaying can be modified with transformations (even for multi language)


    def user_send(self, datapoint):
        print(datapoint.name + ' was set to: ' + str(datapoint.value) + ' (Random Connection Dummy Code to simulate Data Sending)')
