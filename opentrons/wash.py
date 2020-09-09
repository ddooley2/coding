###This script performs the following wash steps for DxSAQ procedure:
###1.
###2.
###3.
###4.
###5.
###6.
###7.
###8.
###9.

from opentrons import robot, containers, instruments
from opentrons.util import environment

robot.connect(robot.get_serial_ports_list()[0])

environment.refresh()
