import random
import os
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from time import sleep

from .constants import (
    C_METER_TO_FEET,
    GES_TO_FSIM_PICTH_SHIFT_DG,
)

def connect_to_flight_sim():
    """
    Create a connection to MSFS via SimConnect.
    Returns:
        sm (SimConnect): The SimConnect connection object
        aq (AircraftRequests): Object for reading aircraft data
        ae (AircraftEvents): Object for sending events (pause, etc.)
    """
    try:
        sm = SimConnect()
        print("Connected to Flight Simulator!\n")
    except Exception as e:
        raise e
    
    aq = AircraftRequests(sm)
    ae = AircraftEvents(sm)

    pause_on = ae.find("PAUSE_ON")
    pause_on()

    return sm, aq, ae


def set_position( sm, altitude_meters, latitude, longitude, airspeed=0, 
                 heading=0, pitch=0, bank=0, on_ground=0):
    """
    Wrapper for sm.set_pos with appropriate corrections
    """
    sm.set_pos(
        _Altitude=altitude_meters * C_METER_TO_FEET,
        _Latitude=latitude,
        _Longitude=longitude,
        _Airspeed=airspeed,
        _Heading=heading,
        _Pitch=-pitch + GES_TO_FSIM_PICTH_SHIFT_DG,
        _Bank=-bank,
        _OnGround=on_ground,
    )
