import random
from .constants import NB_RD_OBJ

def add_objects_on_runway(sm, aq, objlist):
    """
    Add random 3D objects from 'objlist' near the aircraft's current position.
    """
    lat = aq.get("PLANE_LATITUDE")
    lon = aq.get("PLANE_LONGITUDE")
    alti = aq.get("PLANE_ALTITUDE")

    rqst = sm.new_request_id()
    if lat is not None and lon is not None:
        for _ in range(NB_RD_OBJ):
            sign_l = 1 if random.random() < 0.5 else -1
            shiftl = random.randrange(0, 40) * sign_l * random.random() / 10000.0

            sign_L = 1 if random.random() < 0.5 else -1
            shiftL = random.randrange(0, 40) * sign_L * random.random() / 10000.0

            idobj = random.randrange(len(objlist))

            sm.createSimulatedObject(
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
