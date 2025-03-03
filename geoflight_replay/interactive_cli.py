import keyboard

from .constants import (
    default_input_file,
    miscobjlist,
    aircraft_list,
    living_list,
    LFBO_ALT,
    LFBO_LAT,
    LFBO_LON,
    LFBO_HEAD_DG,
    BIRK_LAT,
    BIRK_LON,
    BIRK_ALT,
)
from .simconnect_utils import set_position
from .object_spawner import add_objects_on_runway
from .capture import GES_to_FSIM_runcapture


def print_menu():
    print("\n- Press c to export images from a Google Earth Studio scenario. "
          f"Default scenario file {default_input_file}")
    print("- Press r to run Google Earth Studio scenario. "
          f"Default scenario file {default_input_file}")
    print()
    print("- Press t to go to LFBO airport")
    print("- Press b to go to BIRK airport")
    print()
    print("- Press o to add random airport misc objects")
    print("- Press a to add random aircrafts")
    print("- Press l to add random living things")
    print()
    print("- Press p to pause simulation")
    print("- Press q to quit")
    print()


def interactive_loop(sm, aq, ae):
    """
    Run the interactive loop, watching for keystrokes and calling the right methods.
    """
    print_menu()

    while True:
        try:
            event = keyboard.read_event(True)
        except Exception as e:
            print(f"Error with the keybord read event: {e}")
            raise e
        # Only act on key-down
        if event.event_type != "down":
            continue

        key = event.name

        if key == "q":
            print("QUIT!")
            break

        elif key == "a":
            add_objects_on_runway(sm, aq, aircraft_list)
            print("AIRCRAFTS ADDED!")

        elif key == "l":
            add_objects_on_runway(sm, aq, living_list)
            print("LIVINGS ADDED!")

        elif key in ["c", "r"]:
            scenario_file = input(
                f"Enter YAML scenario file or press ENTER for default [{default_input_file}] : "
            ) or default_input_file

            if key == "c":
                GES_to_FSIM_runcapture(sm, scenario_file, b_save=True)
            else:
                GES_to_FSIM_runcapture(sm, scenario_file, b_save=False)
            
            print_menu()

        elif key == "o":
            add_objects_on_runway(sm, aq, miscobjlist)
            print("MISC. OBJECTS ADDED!")

        elif key == "t":
            set_position(
                sm,
                altitude_meters=LFBO_ALT,
                latitude=LFBO_LAT,
                longitude=LFBO_LON,
                heading=LFBO_HEAD_DG,
                pitch=0,
                bank=0,
                on_ground=0,
            )
            print("Position set to LFBO")

        elif key == "b":
            set_position(
                sm,
                altitude_meters=BIRK_ALT,
                latitude=BIRK_LAT,
                longitude=BIRK_LON,
                heading=0,
                pitch=0,
                bank=0,
                on_ground=0,
            )
            print("Position set to BIRK")

        elif key == "p":
            pause_on = ae.find("PAUSE_ON")
            pause_on()

