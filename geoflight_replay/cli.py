import sys
import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from geoflight_replay.simconnect_utils import connect_to_flight_sim
from geoflight_replay.capture import GES_to_FSIM_runcapture
from geoflight_replay.interactive_cli import interactive_loop
from geoflight_replay.constants import default_input_file


def invite():
    """
    Entry point for geoflight_replay.
    This script determines whether to run in interactive mode or script mode.
    """

    # Connection to Microsoft Flight Simulator
    sm, aq, ae = connect_to_flight_sim()

    # if a YAML scenario is provided as an argument
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        if not os.path.isfile(input_file):
            print(f"Error: No such file or directory: {input_file}")
            return
        GES_to_FSIM_runcapture(sm, aq, ae, input_file, b_save=True)

    else:
        interactive_loop(sm, aq, ae)

    sm.exit()
    print("Goodbye!")
