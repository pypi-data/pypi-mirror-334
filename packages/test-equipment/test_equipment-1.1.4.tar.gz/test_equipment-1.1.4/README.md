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
