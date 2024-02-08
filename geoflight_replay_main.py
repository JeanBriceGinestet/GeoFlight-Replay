"""geoflight_replay_main.py: Replay and capture scenario from Google Earth Studio (YAML format) in Microsoft Flight Simulator."""

__author__ = "Jean-Brice Ginestet"
__license__ = ""
__version__ = "0.15"
__status__ = "Production"

import random
from SimConnect import *
from time import sleep
import dxcam
import yaml
import math
import cv2
import pygetwindow as gw
import random
import keyboard
import os
import sys


default_input_file = "input_samples/BIRK_01_500.yaml"
default_output_dir = "output/"

# Pitch shift between Google Earth Studio and MS Flight Simulator
GES_TO_FSIM_PICTH_SHIFT_DG = 90

C_METER_TO_FEET = 3.280839895

# BIRK airport coordinates
BIRK_LAT = 64.1240145
BIRK_LON = -21.936570
BIRK_ALT = 48.879488

# LFBO coordinates
LFBO_LAT = 43.632023
LFBO_LON = 1.363311
LFBO_ALT = 160 * C_METER_TO_FEET
LFBO_HEAD_DG = 150 # Heading on the LFBO runway

# Default output pciture resolution(virtual camera)
OUTPIC_RES_X_PIX = 2448
OUTPIC_RES_Y_PIX = 2648

# Value to crop on screen capture, depends on screen resolution. Here values for 3840*2160.
DEFAULT_TOP_CROP_PIX = int(38)
DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX = int(8)

# Number of ramdom of objects to add
NB_RD_OBJ = 20

# Time in seconds to wait for 3D data to load.
LOAD3D_WAIT_TIME_S = 20
LOAD3D_INTER_WAIT_TIME_S = 0.4

# 3D miscellaneous aiport object list supported in Microfost Flight Simulator
miscobjlist = [
    "ASO_Baggage_Cart01",
    "ASO_Baggage_Cart02",
    "ASO_Baggage_Loader_01",
    "ASO_BaggageTruck01",
    "ASO_Firetruck01",
    "ASO_Firetruck01",
    "ASO_FuelTruck01_Black",
    "ASO_Ground_Power_Unit",
    "ASO_Pushback_Blue",
    "ASO_Tug01_White",
    "ASO_Tug02_White",
    "ASO_Shuttle_01_Gray",
    "ASO_Catering_Truck_01",
    "ASO_CarUtility01",
    "ASO_TruckUtility01",
    "ASO_Boarding_Stairs",
    "ASO_Boarding_Stairs_Yellow",
    "ASO_Aircraft_Caddy",
    "ASO_CarFacillity01_Black",
    "ASO_CarFacillity01_White",
    "ASO_TruckFacility01_Black",
    "ASO_TruckFacility01_Yellow",
    "windsock",
    "TNCM_Jetway",
]

# 3D aicraft list supported in Microfost Flight Simulator
aircraft_list = [
    "TBM 930 Asobo",
    "Airbus A320 Neo Asobo",
    "Bell 407 Green-Black",
    "Cessna 152 Asobo",
]

# 3D living list supported in Microfost Flight Simulator
living_list = [
    "Marshaller_Male_Summer_Indian",
    "Marshaller_Female_Winter_Caucasian",
    "Marshaller_Female_Summer_African",
    "Marshaller_Male_Winter_Asian",
    "Tarmac_Male_Summer_African",
    "Tarmac_Female_Winter_Arab",
    "Tarmac_Male_Winter_Caucasian",
    "Tarmac_Female_Summer_Hispanic",
    "GrizzlyBear",
    "PolarBear",
    "AfricanGiraffe",
    "ReticulatedGiraffe",
    "Flamingo",
    "Goose",
    "Hippo",
    "Seagull",
    "Pilot_Male_Uniform",
]


# Add random 3D objects on runway (near the plane, if not on a runway)
def add_objects_on_runway(sm, aq, objlist):
    lat = aq.get("PLANE_LATITUDE")
    lon = aq.get("PLANE_LONGITUDE")
    alti = aq.get("PLANE_ALTITUDE")

    rqst = sm.new_request_id()
    if lat != None and lon != None:
        for i in range(NB_RD_OBJ):
            if random.random() < 0.5:
                sign = 1
            else:
                sign = -1

            shiftl = random.randrange(0, 40) * sign * random.random() / 10000.0

            if random.random() < 0.5:
                sign = 1
            else:
                sign = -1

            shiftL = random.randrange(0, 40) * sign * random.random() / 10000.0
            idobj = random.randrange(len(objlist))

            hr = sm.createSimulatedObject(
                objlist[idobj],
                lat + shiftl,
                lon + shiftL,
                rqst,
                hdg=random.randrange(0, 360),
                gnd=1,
                alt=alti,
                pitch=0,
                bank=0,
                speed=0,
            )

# Run and capture a Google Earth Scenario in Microsoft Flight Simulator
def GES_to_FSIM_runcapture(sm, input_file, b_save):
    if b_save:
        print("CAPTURE STARTING!")
    else:
        print("RUN STARTING!")

    # Switch to Flight Simulator Window
    winFS = gw.getWindowsWithTitle("Microsoft Flight Simulator")[0]
    winFS.maximize()
    winFS.activate()
    sleep(0.2)

    # TODO : read pix size from YAML
    # entry = data["image"]
    # campic_res_x_pix = entry.get("width", [])
    # campic_res_y_pix = entry.get("height", [])

    campic_res_x_pix = OUTPIC_RES_X_PIX
    campic_res_y_pix = OUTPIC_RES_Y_PIX

    # Compute scale to match pic size from Google Earth Studio
    newsize = (campic_res_x_pix, campic_res_y_pix)
    campic_ratio = campic_res_x_pix / campic_res_y_pix

    camera = dxcam.create(output_color="BGR")
    screen_res_x_pix = camera.width
    screen_res_y_pix = camera.height

    # To crop Dev mode bar in Flight Simulator, depends on the screen resolution
    top_crop_pix = DEFAULT_TOP_CROP_PIX

    # Bottom screen black bar in Flight Simulator,  depends on the screen resolution
    bottom_black_bar_pix = DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX

    # Adpat output pic to screen res
    if campic_res_y_pix > screen_res_y_pix:
        campic_crop_res_y_pix = screen_res_y_pix - top_crop_pix - bottom_black_bar_pix
        campic_crop_res_x_pix = math.ceil(campic_crop_res_y_pix * campic_ratio)
        bottom_crop_pix = int(screen_res_y_pix - bottom_black_bar_pix)
        left_crop_pix = int((screen_res_x_pix / 2) - (campic_crop_res_x_pix / 2))
        right_crop_pix = int(left_crop_pix + campic_crop_res_x_pix)

    # Define screen region to capture
    left = left_crop_pix
    top = top_crop_pix
    right = right_crop_pix
    bottom = bottom_crop_pix
    region = (left, top, right, bottom)

    # Configure screen region to capture to match Google Earth Studio acquisition
    camera.start(region=region, target_fps=120)

    # Loading yaml input scenario file
    try:
        with open(input_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(e)
        quit()
    print(f"{input_file} loaded!")

    # Create captured pictures output dir if not exist.
    if b_save:
        if not os.path.exists(default_output_dir):
            os.makedirs(default_output_dir)

    id = 0
    for entry in data["poses"]:
        # Get postion and orientation data from input file
        pose = entry.get("pose", [])
        latitude = pose[1] if len(pose) > 1 else ""
        longitude = pose[0] if len(pose) > 0 else ""
        altitude = pose[2] if len(pose) > 2 else ""
        speed = 0
        pitch = pose[4] if len(pose) > 4 else ""
        heading = pose[3] if len(pose) > 3 else ""
        bank = pose[5] if len(pose) > 5 else ""

        # Set aircraft (eq camera) postion and orientation
        sm.set_pos(
            _Altitude=altitude * C_METER_TO_FEET,
            _Latitude=latitude,
            _Longitude=longitude,
            _Airspeed=speed,
            _Heading=heading,
            _Pitch=-pitch + GES_TO_FSIM_PICTH_SHIFT_DG,
            _Bank=-bank,
            _OnGround=0,
        )

        if id == 0:
            if b_save:
                # Wait to load data longer for the first position
                print("WAITING FOR 3D DATA TO lOAD.")
                sleep(LOAD3D_WAIT_TIME_S)
                print("CAPTURING SCENARIO!")
            else:
                print("RUNNING SCENARIO...")
        else:
            # Wait to load 3D world details data between 2 positions
            sleep(LOAD3D_INTER_WAIT_TIME_S)

        # Screen-capture, scale and save acquisition
        if b_save:
            im_str = (
                default_output_dir
                + os.path.splitext(os.path.basename(default_input_file))[0]
                + "_"
                + str(f"{id:03d}")
                + ".png"
            )
            cv2.imwrite(im_str, cv2.resize(camera.get_latest_frame(), newsize))

        id = id + 1

    camera.stop()

    if b_save:
        print("CAPTURE FINISHED!\n")
    else:
        print("RUN FINISHED!\n")

# Print user menu for interactive mode
def print_menu():
    print(f"- Press c to capture a Google Earth Studio scenario.  Default scenario file {default_input_file}")
    print(f"- Press r to run Google Earth Studio scenario. Default scenario file {default_input_file}")
    print()
    print("- Press t to go to LFBO airport")
    print("- Press b to go to BIRK airport")
    print()
    print("- Press o to add random airport misc objects")
    print("- Press a to add random aircrafts")
    print("- Press l to add random living things")
    print()
    print("- Press q to quit")
    print()

def main():

    if len(sys.argv)==2:
        input_file = sys.argv[1] 
        if not os.path.isfile(input_file):
            print(f"Error: No such file or directory : {input_file}")
            quit()
        b_interactive = False
    else:
        b_cont = True
        b_interactive = True

    print(f"Welcome to GeoFlight Replay v{ __version__} !\n")

    # Connection to Flight Simulator
    try:
        sm = SimConnect()
    except Exception as e:
        capture_error = e
        print(e)
        quit()

    print("Connected to Flight Simulator!\n")

    # Set-up Fsim connfiguration
    aq = AircraftRequests(sm)
    ae = AircraftEvents(sm)
    # Set FS simulation in Pause mode
    event_to_trigger = ae.find("PAUSE_ON")
    event_to_trigger()

    # Interactive mode
    if b_interactive:
        print_menu()
        while b_cont == True:
            event = keyboard.read_event(True)
    
            if event.name == "q" and event.event_type == "down":
                b_cont = False
                break
            elif event.name == "a" and event.event_type == "down":
                add_objects_on_runway(sm, aq, aircraft_list)
                print("AIRCRAFTS ADDED!")
            elif event.name == "l" and event.event_type == "down":
                add_objects_on_runway(sm, aq, living_list)
                print("LIVINGS ADDED!")
            elif (event.name == "c" or event.name == "r") and event.event_type == "down":
                input_file = input(f'Enter YAML scenario file or press ENTER for default file [{default_input_file}] : ') or default_input_file
                if not os.path.isfile(input_file):
                    print(f"Error: No such file or directory : {input_file}")
                else:
                    if event.name == "c":
                        b_capture = True
                    else:
                        b_capture = False
                    GES_to_FSIM_runcapture(sm, input_file, b_capture)
            elif event.name == "o" and event.event_type == "down":
                add_objects_on_runway(sm, aq, miscobjlist)
                print("MISC. OBJECTS ADDED!")
            elif event.name == "t" and event.event_type == "down":
                # SET position (LFBO)
                sm.set_pos(
                    _Altitude=LFBO_ALT,
                    _Latitude=LFBO_LAT,
                    _Longitude=LFBO_LON,
                    _Airspeed=0,
                    _Heading=LFBO_HEAD_DG,
                    _Pitch=0,
                    _Bank=0,
                    _OnGround=0,
                )
                print("Positon set to LFBO")
    
            elif event.name == "b" and event.event_type == "down":
                # SET position (BIRK)
                sm.set_pos(
                    _Altitude=BIRK_ALT,
                    _Latitude=BIRK_LAT,
                    _Longitude=BIRK_LON,
                    _Airspeed=0,
                    _Heading=0,
                    _Pitch=0,
                    _Bank=0,
                    _OnGround=0,
                )    
                print("Positon set to BIRK")
    # Script mode
    else:
        GES_to_FSIM_runcapture(sm, input_file, True)
    
    print("QUIT!")
    sm.exit()
    quit()


if __name__ == "__main__":
    main()
