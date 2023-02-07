import math


def make_orbit_block(orbit: int) -> str:
    block = math.floor(orbit / 100) * 100
    return 'orbit' + f'{block}'.zfill(5)


def make_orbit_code(orbit: int) -> str:
    return 'orbit' + f'{orbit}'.zfill(5)
