# System Monitor for Radiation Testing (SMRT)

SMRT is a Python®-based software package intended to monitor computer system performance during radiation testing.

----

**Table of Contents**

[[_TOC_]]

----

# Purpose

This tool is intended to provide a comprehensive, cross-platform (Windows®/Linux®, Intel®/ARM®, etc.) test suite geared towards assessing computer performance as they go through radiation testing.  It's hoped that this will be widely adopted by the aerospace avionics community, creating a common standard for radiation survivability of computers (especially commercial-off-the-shelf single board computers) and that the community will continually improve this tool.

# Questions/Comments/Concerns?

The best way to get these things addressed is to open an issue on GitHub® and/or email the developer (samuel.m.pedrotty@nasa.gov).  Don't hesitate to reach out-- it's likely others also have your questions/comments/concerns.  We encourage users to add capability and fix bugs and then submit merge/pull requests to have their improvements brought back to the repository for all to benefit from.

# Basic Use

1. move the repository to the target computer
2. install Python 3
3. run the install script in the "setup" directory
4. run the start_tests.py script in the py_src directory
    * the test scripts will start assessing the system and logging data to a folder named with the start time in the "data" folder
5. stop the script or shutdown the SBC to terminate the software

# Data Analysis
1. after running the tool, run the "plot_results.py" script in the "py_src" folder to load, concatenate, and plot the data.
    * in some cases, it may be best to transfer the data to a faster computer for analysis and plotting

# Detailed Use

It's assumed that all of the interfaces of the computer under test will be connected appropriately to allow their monitoring (e.g. displays, ethernet, USB devices, etc.).

## Pre-test

1. appropriately install the Operating System on the computer (this software should support Linux and Windows)
2. move the repository to the computer
3. install Python 3
4. run the install script in the "setup" directory
5. update the user input section of the "start_tests.py" script in the "py_src" directory
    * set the *ram_pct_to_use*, the RAM usage parameter with units of percents (< 95% is recommended to provide the OS some headroom)
    * set the *data_save_interval*, the  parameter that determines the time between data file saving with units of seconds (if a high particle flux is to be used, an interval of < 3 seconds is recommended)
    * set the *test_cycle_time*, the parameter that sets the run rate of the test scripts with units of seconds (0.1 is recommended.  Note that some tests will run slower than the rate as their functions take a set time that may be larger than some user-input cycle times)
6. configure the computer as it will be when under test (software and hardware)
7. run the "start_tests.py" script in the "py_src" directory for a couple minutes to verify functionality
    * it's recommended to run the script as 'sudo' on Linux and as administrator on Windows
8. transfer the data to a faster computer that also has Python 3 installed and run the "plot_results.py" script to verify the tool (and computer) functioned as intended
9. delete the pre-test data from the computer to save disk space, keep the set that was moved onto the faster computer as a pre-test artifact

## Test use

10. appropriately deploy the computer in the test environment, connecting all interfaces as briefly mentioned above
11. run the "start_tests.py" script in the "py_src" directory and wait until you see the terminal print stating RAM allocation is complete, and that the cpu, disk, and network monitoring functions are operating
12. start the radiation test (e.g., start the particle flow and other test support equipment)
13. stop the test and/or make note when any off nominal behavior is observed, including unresponsive interfaces, crashed software, or prints stating off-nominal conditions were detected (including RAM changes, disk disconnections, and network adapter disconnections)
    * noting the flux/fluence and failure type will provide insight into the MTBF of that computer subsystem and will inform fault recovery and mitigation design
14. when the test is complete, assuming the device is still functional, transfer the data off and save it as a test artifact
15. plot the data with "plot_results.py" script in the "py_src" directory and review the data for other indicators of faults to inform MTBF analysis


# Detailed Function Description

## install_tool.py

This script automatically installs all of the necessary software requirements for Windows and Linux platforms after Python 3 is installed by the user.  The packages required for data plotting are optional and user-prompted as they can be memory-intensive for small, cheap, computers with limited RAM.

## start_tests.py

This script starts all of the test scripts and provides a regular, 1 Hz print to the terminal to provide a "heartbeat" to indicate if the computer/interface is still functioning.  This script also contains the aforementioned user inputs.

## test_ram.py

This script starts writing 1s to a struct until a user-defined amount of RAM is consumed.  Each cycle, the script will check the struct to make sure it's consistent.  If it's not, it will log an 'upset' and will print *RAM STATE CHANGE DETECTED*.  The RAM will not be overwritten to reset it.  Sometimes restarting the script can reset upsets, but sometimes the whole device must be restarted.  At other times, especially after the unit under test has been subject to a considerable particle flux, upsets may trigger after restarting even when the particle beam is off.  The script also records the percentage of RAM used.

## test_cpu.py

This script records the percentage of CPU used, current frequency in MHz, and CPU temperature in C (temperature is Linux-only).

## test_disks.py

This script records the number of disks/drives detected and will print *NUMBER OF DISKS HAS CHANGED!* if a change in the number of drives is detected.  This script also records some information regarding the drives.

## test_networks.py

This script records the number of network adapters detected and will print *NUMBER OF NETWORK ADAPTERS HAS CHANGED!* if a change in the number of adapters is detected.  This script also records some information regarding the adapters.

## plot_results.py

This script concatenates and loads all data in the most recently created data folder.  It then plots the data and, depending on a user-set flag, can also save the plots and pngs.

# Known Issues and Forward Work
1. The CPU temperature code only works on Linux operating systems.  Windows CPU temp values are hard-coded to 9999
2. The test_disks and test_networks scripts leave much to the user to parse in post-processing.  This should be intelligently handled by the tool.
3. The CPU frequency code only works on Linux operating systems.  Windows CPU frequency values are fixed to the system's base clock speed.

