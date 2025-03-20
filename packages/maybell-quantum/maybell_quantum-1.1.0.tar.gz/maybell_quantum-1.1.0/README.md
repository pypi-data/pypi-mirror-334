# Maybell Quantum API
Public Python API to Maybell Quantum dilution refrigerators.

## Getting Started

```shell
pip install maybell_quantum
```
https://pypi.org/project/maybell-quantum/

### Dependencies
Below are the direct dependencies of this API:

- influxdb-client
- matplotlib (optional)

## Latest Additions
- pymongo support - MongoTimeSeries
- Pandas support - MongoTimeSeries.fetch_pandas returns a pandas.DataFrame

## Coming Soon
- Live plotting.
- User-defined data injection.

## Quick Start for the Impatient

### Cloud Access: 
First off you'll need two things from Maybell Quantum:
1. An API Token (e.g. 'EDECC12...THISouWIS_0oZ_A_P-yFAKE8...ITOKENO...A==')
2. InfluxDB bucket associated with the API Token. (e.g. "Acme Quantum Computers")

### Local Access:
Jump to the [Local Access Guide](/docs/LocalAccess.md) and then come back here.

**Copy and paste the following snippet and save it to a file called** `plot_temperature_data.py`:

NB: The default values for url and org should work fine for all customers.

```python
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging
import os

import matplotlib.pyplot

from maybell_quantum.fridgedb import FridgeDB
from maybell_quantum.fridgedb import TimeRange

from maybell_quantum.helpers import plot
from maybell_quantum.helpers import pretty_print_result

if "INFLUXDB_TOKEN" not in os.environ:
    logging.fatal(
        "INFLUXDB_TOKEN environment variable is not set.  Can't connect without it."
    )
    exit(1)
token = os.environ["INFLUXDB_TOKEN"]
# TODO: edit the following line with your bucket name
bucket = "<maybell-assigned-bucket-name>"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
org = "Maybell Quantum"

fdb = FridgeDB(org=org, url=url, token=token, bucket=bucket)

stop_time = datetime.now(timezone.utc)
start_time = stop_time - timedelta(hours=10)
time_range = TimeRange(start_time, stop_time)

matplotlib.pyplot.figure()
thermometers = ["mxp"]
temperatures = fdb.fetch(time_range, thermometers)
plot(thermometers, "temperature", temperatures, saveas="temperatures.png")
pretty_print_result(temperatures)
```

```sh
export INFLUXDB_TOKEN=<your-company-token>
python3 plot_temperature_data.py
```

### Using Local Timezone

We recommend users manage queries using Coordinated Universal Time (UTC). The frigdedb `TimeRange` dataclass must be in UTC. Daylight savings rollovers or rollbacks can result in queries for more or less data than you may expect. However, for small sessions where it may be convenient, you can provide time ranges in local time using Timezone-Aware `datetime`. Use `zoneinfo.available_timezones()` to see a list of supported regions. 

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

tz = ZoneInfo("America/Los_Angeles")

# create a Timezone-Aware `datetime` object using the tzinfo parameter
start_time_local = datetime(year=2024, month=12, day=4, hour=6, tzinfo=tz)
start_time_utc = start_time_local.astimezone(ZoneInfo("UTC"))  # UTC conversion
stop_time_utc = start_time_local + timedelta(8)

time_range = TimeRange(start_time_utc, stop_time_utc)
```

### In More Detail (Optional)

```python
from fridgedb import FridgeDB
org = 'Maybell Quantum'
url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
token = 'EDECC12GXgRO8grdiLPD7tXUVY7QL36THISouWIIS_0oZ_4SAfP-yFAKE8I3ZFBg0TOKENOko1fZikpEmq43gA=='
bucket = 'Acme Quantum Computing'
fdb = FridgeDB(org=org, url=url, token=token, bucket=bucket)
```

#### Get Temperature Data

You'll need to know the names of the thermometers for your specific system.  Typical
values are currently hard-coded as static class variables in FridgeDB.

```python
from fridgedb import FridgeDB, TimeRange
from helpers import pretty_print_result, plot 
from datetime import datetime, timedelta, timezone
print(f"{FridgeDB.sensor_names}")
print(f"{FridgeDB.device_names}")
org = 'Maybell Quantum'
url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
token = '<your_api_token>'
bucket = '<your_maybell_assigned_bucket>'
fdb = FridgeDB(org=org, url=url, token=token, bucket=bucket)
time_range = TimeRange(start_time=datetime.now(timezone.utc) - timedelta(minutes=45), stop_time=datetime.now(timezone.utc))
thermometers = ["mxp", "prp", "rgp", "stp"]
temperatures = fdb.fetch(time_range, thermometers)
plot(thermometers, 'temperature', temperatures, saveas="temperatures.png")
pretty_print_result(temperatures)
```

##### Step by Step Explanation

Start with importing the necessary classes and some helper functions, like `pretty_print_result` and `plot`.
Next set the variable needed to create, and pull data from, an InfluxDB client.  NB: you'll need
to get a unique API token from Maybell, as well as the name of the bucket(s) for your fridge(s).
```shell
In [1]: from fridgedb import FridgeDB, TimeRange
   ...: from helpers import pretty_print_result, plot
   ...: from datetime import datetime, timedelta
In [2]: org = 'Maybell Quantum'
   ...: url = 'https://us-east-1-1.aws.cloud2.influxdata.com'
   ...: token = '<your_api_token>'
   ...: bucket = '<your_maybell_assigned_bucket>'
```

Now that we have an instance of FridgeDB we can fetch data.  The TimeRange dataclass has just two members: 
`start_time` and `stop_time` (both Python datetime objects).  Below is an example of how to fetch
data for the last 45 minutes.
```shell
In [3]: fdb = FridgeDB(org=org, url=url, token=token, bucket=bucket)
   ...: time_range = TimeRange(start_time=datetime.utcnow() - timedelta(minutes=45), stop_time=datetime.utcnow())
   ...: temperatures = fdb.fetch(time_range, ["mxp", "prp", "rgp", "stp"])
   ...: print(f"{fdb.sensor_names}")
   ...: print(f"{fdb.device_names}")
['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'cfp', 'f1', 'icp', 'mxp', 'prp', 'rgp', 'stp']
['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17', 'v18', 'v19', 'v20', 'v21', 'v22', 'v23', 'v24', 'v25', 'v26', 'pm1', 'pm2', 'pm3', 'pm4', 'pm5', 'warmup', 'still', 'sample', 'cp1', 'cp2', 'inv1']
```

The result that's returned is a dictionary of dictionaries, where the first key is the name of the
device or sensor, and the second key is the field of interest (e.g. "temperature").  Below shows
the structure in more detail for clarity.

```shell
In [4]: pretty_print_result(temperatures)
{ 'mxp' : 
    {
        'power' = [46.73, 49.89,..., 2.12, 57.52]
        'quadrature' = [37.34, 68.39,..., 10.02, 40.96]
        'resistance' = [62.17, 19.55,..., 25.76, 26.95]
        'temperature' = [77.86, 4.62,..., 58.08, 39.46]
    }
}
{ 'prp' : 
    {
        'power' = [57.88, 35.83,..., 84.21, 20.50]
        'quadrature' = [2.24, 52.69,..., 66.20, 94.42]
        'resistance' = [92.64, 11.34,..., 59.66, 80.26]
        'temperature' = [74.98, 6.59,..., 4.66, 24.80]
    }
}
{ 'rgp' : 
    {
        'power' = [93.86, 96.91,..., 53.15, 49.18]
        'quadrature' = [61.12, 98.45,..., 66.95, 98.52]
        'resistance' = [58.18, 30.39,..., 66.84, 41.51]
        'temperature' = [5.97, 15.57,..., 37.27, 38.87]
    }
}
{ 'stp' : 
    {
        'power' = [1.99, 65.45,..., 49.96, 85.84]
        'quadrature' = [58.32, 6.96,..., 18.05, 69.87]
        'resistance' = [55.72, 30.75,..., 68.62, 15.45]
        'temperature' = [17.65, 39.26,..., 58.94, 28.07]
    }
}
```

#### Get All Sensor Data
For convenience, a thin wrapper around `fetch`  is provided that gets all the sensor and device data for a given time range.

```python
machine_state = fdb.fetch_all(time_range)
```

##### Get All Sensor Data Since a Given Time 
For convenience, another thin wrapper around `fetch`  is provided that gets all the sensor and device data from now until `<timedelta>`.

The following snippets pulls the entire machine state (all devices and sensors) for the last hour.
```python
since = datetime.timedelta(hours=1)
machine_state = fdb.last(since)
```

## Details - Sensor and Device Data Model

Snapshots of the fridge state are stored in an InfluxDB database at set
intervals (default is every 10s).

Each system consists of sensors and devices.  Sensors are read-only (e.g. pressure gauges and thermometers) 
and devices can be issued commands (e.g. valves can be opened and closed).

### Sensors
All sensors below have their `_tag` set to "sensor" 
(see [InfluxDB Tags](https://docs.influxdata.com/influxdb/cloud/reference/key-concepts/data-elements/#tags)).

#### Thermometer

```python
{
    "_type" : "thermometer", 
    "_tag": "sensor",
    "temperature": float,
    "resistance": float,
    "quadrature": float,
    "power": float,
}
```

#### Pressure

```python
{
    "_type" : "pressure", 
    "_tag": "sensor",
    "pressure": float,
}
```

#### BGA - Binary Gas Analyzer

```python
{ 
    "_type" : "bga", 
    "_tag": "sensor",
    "percent": float
}
```

#### Flow

```python
{
    "_type" : "flow", 
    "_tag": "sensor",
    "pressure": float,
    "temperature": float,
    "volumetric_flow": float,
    "mass_flow": float,
}
```


### Devices
All devices below have their `_tag` set to "device" 
(see [InfluxDB Tags](https://docs.influxdata.com/influxdb/cloud/reference/key-concepts/data-elements/#tags)).

#### Valve

```python
{
    "_type" : "valve", 
    "_tag": "device",
    "open": bool,
}
```

#### Trap

```python
{
    "_type" : "trap", 
    "_tag": "device",
    "output": float,
}
```


### Pump

```python
{
    "_type" : "pump", 
    "_tag": "device",
    "active": bool,
}
```

### Heater

```python
{
    "_type" : "", 
    "_tag": "device",
    "power": float,
    "current": float,
    "voltage": float,
    "native": float,
}
```

### Loop

```python
{
    "_type" : "loop", 
    "_tag": "device",
    "setpoint": float,
    "gain": float,
    "integral": float,
    "derivative": float,
    "ramp_rate": float,
    "state": bool,
}
```

### Turbo

```python
{
    "_type" : "turbo", 
    "_tag": "device",
    "state": bool,
    "speed": int,
    "converter": int,
    "motor": int,
    "bearing": int,
    "setpoint": int,
    "voltage": int,
    "error": bool,
}
```

### Ecodry

```python
{
    "_type" : "ecodry", 
    "_tag": "device",
    "setpoint": float,
    "frequency": float,
    "current": float,
    "voltage": float,
    "bus_voltage": float,
    "power": float,
    "state": bool,
}
```

### Inverter

```python
{
    "_type" : "inverter", 
    "_tag": "device",
    "state": bool,
    "frequency": float,
    "current": float,
    "voltage": float,
    "alarm": Alarm,
}
```

```python
class Alarm(enum.Enum):
    """Enumerate the toshiba alarm flags."""

    NO_ALARM = 0
    ALARM_OVER_CURRENT = 1 << 0
    ALARM_INVERTER_OVERLOAD = 1 << 1
    ALARM_MOTOR_OVERLOAD = 1 << 2
    ALARM_OVERHEAT = 1 << 3
    ALARM_OVER_VOLTAGE = 1 << 4
    ALARM_UNDER_VOLTAGE = 1 << 5
    ALARM_MAIN_OVERLOAD = 1 << 6
    ALARM_LOW_CURRENT = 1 << 7
    ALARM_OVER_TORQUE = 1 << 8
    ALARM_BRAKE_OVERLOAD = 1 << 9
    ALARM_OPERATION_HOURS = 1 << 10
    ALARM_OPTION_COMMUNICATION = 1 << 11
    ALARM_SERIAL_COMMUNICATION = 1 << 12
    ALARM_MAIN_VOLTAGE = 1 << 13
```

### Compressor

```python
{
    "_type" : "compressor", 
    "_tag": "device",
    "state": bool,
    "discharge_temperature": float,
    "outlet_tempertaure": float,
    "inlet_temperature": float,
    "return_pressure": float,
}
```






