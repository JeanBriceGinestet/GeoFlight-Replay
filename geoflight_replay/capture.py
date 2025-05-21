import os
import cv2
import yaml
import json
import random
import dxcam
from time import sleep
from PIL import Image

from .windows_utils import show_available_windows, activate_and_maximize_window
from .simconnect_utils import set_position
from .constants import (
    default_output_dir,
    DEFAULT_TOP_CROP_PIX,
    DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX,
    CHANGE_AIRPORT_DELAY,
    CHANGE_RUNWAY_DELAY,
    BASE_DELAY
)

glob_current_airport = "" # Variable to store current airport in case of error, to be able to restart from that same airport

def load_scenario(input_file):
    """
    Reads the YAML scenario file and returns the parsed data.
    """
    try:
        with open(input_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML file '{input_file}': {e}")
        return None
    return data


def initialize_camera():
    """
    Initializes and returns a dxcam camera instance (output_color='BGR').
    """
    print("-- Starting dxcam --")
    return dxcam.create(output_color="BGR")


def validate_scenario_fits(scenario_width, scenario_height, available_width, available_height):
    """
    Raises ValueError if the scenario resolution doesn't fit the available area.
    """
    if scenario_width > available_width or scenario_height > available_height:
        raise ValueError(
            f"Scenario resolution {scenario_width}×{scenario_height} doesn't fit in the available screen space {available_width}×{available_height}."
        )


def compute_top_left_capture_region(scenario_width, scenario_height, screen_width, screen_height):
    """
    Computes the screen region from which images will be captured.
    Returns (left, top, right, bottom).
    """
    available_width = screen_width
    available_height = screen_height - DEFAULT_TOP_CROP_PIX - DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX

    validate_scenario_fits(scenario_width, scenario_height, available_width, available_height)

    left = 1
    top = DEFAULT_TOP_CROP_PIX
    right = left + scenario_width
    bottom = top + scenario_height

    return (left, top, right, bottom)


def replay_poses(poses, sm, aq, ae, camera, region, b_save, output_dir, filename, from_airport = ""):
    """
    Loops through the poses to set position/time and captures frames if requested.
    Start from from_airport if specified. (case of error)
    """
    
    event_to_trigger = ae.find("PAUSE_ON")
    event_to_trigger()
    sleep(0.5)

    total_poses = len(poses)
    num_digits = len(str(total_poses))

    prev_airport = None
    prev_runway = None

    if b_save:
        print("Capture started.")
    else:
        print("Run started (no image saving).")

    for i, entry in enumerate(poses):
        # Handling case where we defined a specific airport to start from
        if from_airport != "" and from_airport !=  entry.get("airport", ""):
            continue
        elif from_airport == entry.get("airport", ""):
            from_airport = ""

        pose_data = entry.get("pose", [])
        if len(pose_data) < 6:
            print(f"Skipping pose index={i}, incomplete data.")
            continue

        lon, lat, alt, heading, pitch, bank = pose_data
        current_airport = entry.get("airport", "")

        global glob_current_airport
        glob_current_airport = current_airport

        current_runway = entry.get("runway", "")


        first_pose = False
        set_position(sm, alt, lat, lon, heading=heading, pitch=pitch, bank=bank)
        
        sleep(0.2)

        current_date = entry.get("time")
        current_hour = current_date.get("hour")
        event_clock = ae.find("CLOCK_HOURS_SET")
        event_clock(current_hour)
        if i == 0:
            if b_save:
                print("Waiting for first airport area to load...")
                first_pose = True
                sleep(CHANGE_AIRPORT_DELAY)
                print("Capturing scenario start...")
            else:
                print("Running scenario start...")
        else:
            if current_airport != prev_airport:
                print(f"Switching airport to {current_airport}...")
                first_pose = True
                sleep(CHANGE_AIRPORT_DELAY)
            elif current_runway != prev_runway:
                print(f"Switching runway to {current_runway}...")
                sleep(CHANGE_RUNWAY_DELAY)
            else:
                sleep(BASE_DELAY)

        sleep(0.1)


        if first_pose:      # Replaying first pose of each airport due to uncontrollable issues occuring sporadically in FLight Simulator
            set_position(sm, alt, lat, lon, heading=heading, pitch=pitch, bank=bank)
            event_clock(current_hour)
            sleep(BASE_DELAY + 1)

        if b_save:
            frame = camera.grab(region)
            if frame is None:
                print(f"[WARNING] No frame returned at index {i}.")
            else:
                out_path = os.path.join(
                    output_dir, f"{filename}_{i:0{num_digits}d}.png"
                )
                cv2.imwrite(out_path, frame)
                print(f"Saved: {out_path}")

        prev_airport = current_airport
        prev_runway = current_runway

    glob_current_airport = "FINISHED"
    if b_save:
        print("Capture finished.\n")
    else:
        print("Run finished.\n")


def GES_to_FSIM_runcapture( sm, aq, ae, input_file, b_save, window_title="Microsoft Flight Simulator", rework_altitude=False):
    """
    Replays a Google Earth Studio scenario in Flight Simulator (or any target window) and
    optionally saves captures. Splits tasks into dedicated helper functions for clarity.
    """

    # Load the scenario
    data = load_scenario(input_file)

    if data is None:
        return  # error already printed in load_scenario
    
    filename = os.path.splitext(os.path.basename(input_file))[0]
    print(f"{filename} loaded from {input_file}!")

    camera = initialize_camera()

    img_info = data.get("image", {})
    zoom_value = img_info.get("fov_x")
    scenario_width = img_info.get("width", 1024)
    scenario_height = img_info.get("height", 1024)
    print(f"   Expecting a fov of: {zoom_value}.")
    print(f"Scenario expects size: {scenario_width}×{scenario_height}")

    if not activate_and_maximize_window(window_title, scenario_width, scenario_height):
        return
    
    screen_width = camera.width
    screen_height = camera.height

    # Compute capture region
    region = compute_top_left_capture_region( scenario_width, scenario_height, screen_width, screen_height)

    print(
        f"Capturing region: {region}, \n"
        f"         Screen = {screen_width}×{screen_height}, \n"
        f"          Avail = {screen_width}×{screen_height - DEFAULT_TOP_CROP_PIX - DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX}"
    )

    output_dir = os.path.join(default_output_dir, filename)
    if b_save:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Capture directory: {output_dir}")

    poses = data.get("poses", [])

    global glob_current_airport
    glob_current_airport = ""  # Parameter to change to start from a specific airport, or "" to start fromt the beginning

    while (glob_current_airport != "FINISHED"):
        try:
            replay_poses(poses, sm, aq, ae, camera, region, b_save, output_dir, filename, glob_current_airport)
        except KeyboardInterrupt:
            glob_current_airport = "FINISHED"
        except:
            print(f"[HANDLED-ERROR] Restarting at airport {glob_current_airport}.")

    # camera.stop()
    print("       --- Scenario completed. ---")
    sleep(1)