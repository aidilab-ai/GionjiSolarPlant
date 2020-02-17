import adc

IRRADIANCE = adc.A5

LIGHT_SCALE = 1
LIGHT_MEASURE_UNIT = 'lumen'

def getIrradiation():
    val = adc.readAdc(IRRADIANCE)
    value = val * LIGHT_SCALE
    return value