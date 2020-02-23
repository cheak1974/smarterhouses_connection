**Documentation for Connection Module Homematic**

_Author: Christian Küken_

_Version: 1.0_

_Used Libraries: PyHomematic by Daniel Perna_

**Instance creation for Homematic**

`Add a file like my_homematic_connection.py in /config/connections`

`Add a line in this file to create an instance of the Connection:`


```python
# ./config/connections/my_homematic_connection.py
import core.globals
import connection.homematic.homematic

core.globals.pool['conn']['homematic'] = connection.homematic.homematic.Homematic(name='homematic', friendly_name='Homematic', interval=5.0, ccu_address='192.168.10.21')

# you can add as much connections as you are needing
```

The key for the Dict `core.globals.pool['conn'][KEY]` has to be identical with the content of the name argument.

|Argument                 |Default               |Description            |
|-------------------------|----------------------|-----------------------|
|name                     | --                   |Lowercase Name of the Connection instance without blanks.            |
|friendly_name            | --                   |Meaningful Description which is used for GUI.                        |
|interval                 | 1.0                  |Interval for polling in seconds. If set to None no frequent polling will happen, but only manual receive. |
|local_port               | 7080                 |Port on smarterhouses side for communication |
|ccu_address              | '0.0.0.0'            |IP Address of the CCU2 as String |
|ccu_port                 | 2001                 |Network Port of the CCU2 for communication |


**Arguments for creation of Datapoint Instances**
