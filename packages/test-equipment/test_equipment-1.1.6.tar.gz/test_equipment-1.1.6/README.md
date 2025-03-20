# Test Equipment
This python module allows the user to control the following test equipment via a
USB connection. The test_equipment python module is primarily aimed at providing
an easy way of interfacing with test equipment.

## DC Power Supplies

- HMP2030 PSU
- TENMA 72-2550 PSU
- ETMXXXXP

The psu_ctrl command line tool is installed when this python package is installed.
It is not aimed at being a fully functional tool to control the power supplies but
to provide example code that details how a user may incorporate PSU control into
their applications.

Before using psu_ctrl to control power supplies the configuration must be set using
the 'psu_ctrl -c' command line options. This should be executed with the power supply
connected to the PC. The user should then set parameter 1 to set the power supply
type connected and set parameter 2 to set the PSU connection string.

Once configured the user can turn PSU outputs on/off and set voltages and current
limits.

Command line help is available for the psu_ctrl command line tool as shown below.

```
usage: psu_ctrl.py [-h] [-d] [-c] [-v VOLTS] [-a AMPS] [-o OUTPUT] [--on] [--off] [-r]

A description of what it does.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debugging.
  -c, --config          Configure the PSU parameters.
  -v VOLTS, --volts VOLTS
                        Set PSU voltage (default=3.3).
  -a AMPS, --amps AMPS  Set PSU current limit (default=1.0).
  -o OUTPUT, --output OUTPUT
                        The PSU output to use (default=1).
  --on                  Turn the output on.
  --off                 Turn the output off.
  -r, --read            Read the output current/power.

Supported Power Supplies
Type   Description
0      Dummy PSU
1      HMP2030 PSU
2      TENMA 72-2550 PSU
3      ETMXXXXP
```

# Digital Multimeters

### R&S HM8112-3 Precision Multimeter

The dmm_hm8112 command provides an interface to this meter via a US port.

```
dmm_hm8112 -h
usage: dmm_hm8112 [-h] [-d] [-l] [--port PORT] [-s] [-f FUNCTION] [-p PARAMETER] [-g]

A command line interface to a R&S (Hameg) 8112-3 6.5 digit precision multimeter.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debugging.
  -l, --list_args       List the valid commands.
  --port PORT           The serial port to use. If left blank the first serial port found will be used.
  -s, --send            Send a command to the meter.
  -f FUNCTION, --function FUNCTION
                        The required function.
  -p PARAMETER, --parameter PARAMETER
                        The parameter passed to the function.
  -g, --get             Read any data being sent on the serial port.
```

### OWON AC/DC Clamp Ammeter

The cm2100b command provides an interface to this meter via bluetooth.

```
cm2100b -h
usage: cm2100b [-h] [-d] [-m MAC] [-r] [-l]

An interface to the CM2100B current clamp DMM.

options:
  -h, --help         show this help message and exit
  -d, --debug        Enable debugging.
  -m MAC, --mac MAC  The bluetooth MAC address of the CM2100B meter.
  -r, --read         Read values from the CM2100B over bluetooth.
  -l, --list         List bluetooth devices.
```
