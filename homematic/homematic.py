import core.connection
import core.globals
import sys
import time

sys.path.append(sys.path[0] + '//connection//homematic/lib')            # Maybe not a good idea because of different versions of the packages
#import connection.homematic.lib.pyhomematic.connection as pyhomematic
import pyhomematic

connection_description =    'Connection for connecting to the Homematic Smarthome System via CCU'
connection_version =        '0.01'
connection_author =         'Christian Kueken, Germany'
connection_library =        'pyhomematic by Daniel Perna. (github: danielperna84 / https://github.com/danielperna84/pyhomematic'

connection_parameters = {'interval':    'Interval time. How often (in seconds) will a new number be generated. None if no automatic receiving should happen.',
                         'local_port':  'Network Port smarterhouses shall listen on',
                         'ccu_address': 'IP Address of the CCU2 Device',
                         'ccu_port':    'Network Port the CCU device is listening on'}

connection_datapoint_parameters  = {'hm_address': 'The Homematic Device Address of the Device with this datapoint',
                                    'hm_channel': 'The channel of the device which is equal to the datapoint e.g. LEVEL, STATE, MOTION, BRIGHTNESS. Refer to Homematic Docs.'}

class Homematic(core.connection.Connection):

    def __init__(self, name=None, friendly_name=None, interval=1.0, local_port=7080, ccu_address=None, ccu_port=2001):

        super().__init__(name, friendly_name, interval)        # Init core.connection.Connection

        while True:                         # Loop is only needed in order to end the process with break which only works in loops
            try:
                print("Try connecting to Homematic CCU2...")
                self.hm = pyhomematic.HMConnection(interface_id='smarterhouses', local=core.globals.pool['conf']['server_ip'], localport=local_port, remote=ccu_address, remoteport=ccu_port)
                self.hm.start()

            except:
                print("Error connecting to Homematic CCU2...")
                core.globals.bus.emit('log_error', 'Error while init in Connection <' + self.name + '>', threads=True)
                self.status='error'
                break

            timeout = 0
            while len(self.hm.devices['default']) == 0 and timeout < 5:
                print("Waiting for Homematic devices to come up...")
                timeout = timeout + 1
                time.sleep(1)

            if len(self.hm.devices['default']) > 0:                                     # If the Init was successful we set the status of the service to stopped.
                print("Found Homematic Devices: " + str(self.hm.devices))

                for devicekey, deviceobj in self.hm.devices['default'].items():         # Set the same EventCallback for Devices
                    deviceobj.setEventCallback(self.EventCallback)

                self.status = 'stopped'                                                 # Finally set status to stopped. Needed status for start()

            else:
                print("Error connecting to Homematic CCU2. No Devices found.")
                core.globals.bus.emit('log_error', 'Error while init in Connection <' + self.name + '> no Devices found.', threads=True)
                self.status = 'error'

            break


    def user_receive(self):

        for dp_key, dp_obj in core.globals.pool['data'].items():                                # Iterate all datapoints

            if dp_obj.conn == self:                                                             # Check if actual dp belongs to this connection object

                if dp_obj.conn_para['hm_address'] in self.hm.devices['default'].keys():         # Is this address known to the homematic device instance?
                    #print('USER RECEIVE: ' + str(self.hm.devices['default'][dp_obj.conn_para['hm_address']].getValue(dp_obj.conn_para['hm_channel'])))         #REMOVE
                    # Receive the Value from hm_address with hm_channel and set the datapoint raw value.
                    dp_obj.setValue(self.hm.devices['default'][dp_obj.conn_para['hm_address']].getValue(dp_obj.conn_para['hm_channel']), RawValue=True, SetByConn=True)


    def user_send(self, datapoint):

        alreadyset = False

        # SPECIAL COMMANDS FOR SPECIAL DEVICES

        # Steuerung der Jalousien
        if isinstance(self.hm.devices['default'][datapoint.conn_para['hm_address']], pyhomematic.devicetypes.actors.Blind):
            if datapoint.raw == 'up':
                self.hm.devices['default'][datapoint.conn_para['hm_address']].move_up()
                alreadyset = True
            if datapoint.raw == 'down':
                self.hm.devices['default'][datapoint.conn_para['hm_address']].move_down()
                alreadyset = True
            if datapoint.raw == 'stop':
                self.hm.devices['default'][datapoint.conn_para['hm_address']].stop()
                alreadyset = True

        # Common way to send a Homematic variable (hm_channel) to the device, vie setValue(CHANNEL, VALUE)
        if alreadyset == False:
            self.hm.devices['default'][datapoint.conn_para['hm_address']].setValue(datapoint.conn_para['hm_channel'], datapoint.raw)


    def EventCallback(self, address, interface_id, key, value):

        print('EVENT: ' + address + ' ' + key + ' ' + value)

        for dpkey, dpobj in core.globals.pool['data']:
            if dpobj.conn_para['hm_channel'] == key:
                dpobj.setValue(value, RawValue=True, SetByConn=True)
