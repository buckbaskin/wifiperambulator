
def distance_model(dBm):
    return math.pow(math.e, (dBm+30.35)/-7.82)
