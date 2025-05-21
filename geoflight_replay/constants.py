__author__ = "Jean-Brice Ginestet, Vincent Mussot"
__license__ = "MIT"
__version__ = "0.9"
__status__ = "Production"

# ================================
# Global Constants & Configuration
# ================================
default_input_file = "input_samples/VIDP-9-27.yaml"
default_output_dir = "output/"

# Pitch shift between Google Earth Studio and MS Flight Simulator
GES_TO_FSIM_PICTH_SHIFT_DG = 90

C_METER_TO_FEET = 3.280839895

# BIRK airport coordinates
BIRK_LAT = 64.1240145
BIRK_LON = -21.936570
BIRK_ALT = 9

# LFBO coordinates
LFBO_LAT = 43.632023
LFBO_LON = 1.363311
LFBO_ALT = 160
LFBO_HEAD_DG = 150  # Heading on the LFBO runway

# Default output picture resolution
OUTPIC_RES_X_PIX = 1920
OUTPIC_RES_Y_PIX = 1080

# Crop on screen capture
DEFAULT_TOP_CROP_PIX = 31
DEFAULT_BOTTOM_BLACK_BAR_CROP_PIX = 80

# Number of random objects to add
NB_RD_OBJ = 20

# Time in seconds to wait for 3D data to load
CHANGE_AIRPORT_DELAY = 35  # sec
CHANGE_RUNWAY_DELAY =  4  # sec
BASE_DELAY =           2  # sec

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

