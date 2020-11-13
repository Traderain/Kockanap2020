class CargameAux:
    def __init__(self):
        pass

    def report(self, speed, angle, tryputminedown, tryshootrocket):
        if speed > 20 or speed < 0:
            raise Exception("Invalid speed!")
        if angle < 0 or angle > 35:
            raise Exception("Invalid angle!")
        payload = bytearray()
        payload.append(speed)
        payload.append(angle)
        payload.append(tryputminedown)
        payload.append(tryshootrocket)
        if not len(payload) == 4:
            raise Exception("Mallformed payload!")
        return payload