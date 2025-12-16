"""
Digital Twin physics engine for a wind turbine.
Computes performance metrics and health indicators from SCADA data.
"""

import math
import config


def compute_physics(scada):
    """
    Compute physics-based Digital Twin quantities from SCADA inputs.

    Parameters
    ----------
    scada : dict
        One snapshot of SCADA sensor data.

    Returns
    -------
    dict
        Derived Digital Twin parameters.
    """

    wind = scada["wind_speed"]
    rpm = scada["rpm"]
    power = scada["power"]

    # --- Angular speed ---
    omega = 2.0 * math.pi * rpm / 60.0  # rad/s

    # --- Available wind power ---
    if wind > 0.0:
        p_wind = 0.5 * config.AIR_DENSITY * config.ROTOR_AREA * wind**3
    else:
        p_wind = 0.0

    # --- Tip Speed Ratio ---
    if wind > 0.1:
        tsr = omega * config.ROTOR_RADIUS / wind
    else:
        tsr = 0.0

    # --- Power coefficient ---
    if p_wind > 1.0:
        cp = power / p_wind
        cp = min(cp, config.CP_MAX)
    else:
        cp = 0.0

    # --- Mechanical torque ---
    if omega > 0.1:
        torque = power / omega
    else:
        torque = 0.0

    return {
        "omega": omega,
        "p_wind": p_wind,
        "tsr": tsr,
        "cp": cp,
        "torque": torque
    }


def evaluate_health(scada, dt):
    """
    Evaluate simple health conditions based on SCADA and DT metrics.

    Returns
    -------
    dict
        Health status flags.
    """

    health = {
        "generator_temp": "OK",
        "gearbox_temp": "OK",
        "vibration": "OK",
        "performance": "OK"
    }

    # --- Generator temperature ---
    if scada["gen_temp"] > config.GEN_TEMP_CRIT:
        health["generator_temp"] = "CRITICAL"
    elif scada["gen_temp"] > config.GEN_TEMP_WARN:
        health["generator_temp"] = "WARN"

    # --- Gearbox temperature ---
    if scada["gb_temp"] > config.GB_TEMP_CRIT:
        health["gearbox_temp"] = "CRITICAL"
    elif scada["gb_temp"] > config.GB_TEMP_WARN:
        health["gearbox_temp"] = "WARN"

    # --- Vibration ---
    if scada["vibration"] > config.VIB_CRIT:
        health["vibration"] = "CRITICAL"
    elif scada["vibration"] > config.VIB_WARN:
        health["vibration"] = "WARN"

    # --- Performance degradation ---
    if dt["cp"] < 0.25 and scada["wind_speed"] > config.CUT_IN_WIND:
        health["performance"] = "WARN"

    return health
