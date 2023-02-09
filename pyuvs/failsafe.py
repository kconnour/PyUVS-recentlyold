

def get_apoapse_muv_failsafe_voltage(orbit: int) -> float:
    if orbit < 7857:
        voltage = 497.63803
    else:
        voltage = 515.206
    return voltage
