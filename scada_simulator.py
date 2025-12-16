"""
SCADA data simulator for a wind turbine.
Generates physically believable sensor values at 1-second intervals.
"""

import random
import math
import config



def initialize_state():
    """Initialize turbine SCADA state."""
    return {
        "wind_speed": 8.0,        # m/s
        "rpm": 8.0,               # rotor speed
        "pitch": 2.0,             # degrees
        "power": 0.0,             # watts
        "gen_temp": 40.0,         # °C
        "gb_temp": 45.0,          # °C
        "vibration": 2.5          # mm/s RMS
    }


def step(state):
    """
    Advance the turbine state by one second.
    Returns updated SCADA state.
    """

    # --- 1. Wind speed (master variable) ---
    wind_noise = random.uniform(-0.2, 0.2)
    wind_drift = random.uniform(-0.02, 0.02)
    wind = max(0.0, state["wind_speed"] + wind_noise + wind_drift)

    # --- 2. Rotor speed (controlled response) ---
    if wind < config.RATED_WIND:
        rpm = min(config.MAX_RPM, 1.5 * wind)
    else:
        rpm = config.MAX_RPM

    rpm = max(config.MIN_RPM, rpm)

    # --- 3. Pitch angle (power control) ---
    if wind <= config.RATED_WIND:
        pitch = config.MIN_PITCH + random.uniform(0.0, 0.3)
    else:
        pitch = min(
            config.MAX_PITCH,
            state["pitch"] + random.uniform(0.1, 0.3)
        )

    # --- 4. Power output (measured SCADA value) ---
    if wind < config.CUT_IN_WIND:
        power = 0.0
    else:
        p_wind = 0.5 * config.AIR_DENSITY * config.ROTOR_AREA * wind**3
        power = min(config.RATED_POWER, config.EFFICIENCY * 0.4 * p_wind)

    # --- 5. Generator temperature (thermal inertia) ---
    gen_temp = state["gen_temp"] + 0.01 * (power / config.RATED_POWER * 80 - state["gen_temp"])

    # --- 6. Gearbox temperature ---
    gb_load = (power / config.RATED_POWER) + (rpm / config.MAX_RPM)
    gb_temp = state["gb_temp"] + 0.008 * (gb_load * 90 - state["gb_temp"])

    # --- 7. Vibration RMS ---
    vib = state["vibration"] + random.uniform(-0.02, 0.02)

    return {
        "wind_speed": wind,
        "rpm": rpm,
        "pitch": pitch,
        "power": power,
        "gen_temp": gen_temp,
        "gb_temp": gb_temp,
        "vibration": max(0.5, vib)
    }
