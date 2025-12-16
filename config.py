# ==============================
# Wind Turbine Digital Twin
# Configuration File
# ==============================

# --- Environmental constants ---
AIR_DENSITY = 1.225          # kg/m^3 (sea-level standard)

# --- Turbine geometry ---
ROTOR_RADIUS = 40.0           # meters
ROTOR_AREA = 3.1416 * ROTOR_RADIUS**2

# --- Power ratings ---
RATED_POWER = 2_000_000       # Watts (2 MW)
EFFICIENCY = 0.92             # electrical + mechanical efficiency

# --- Wind speed limits ---
CUT_IN_WIND = 3.0             # m/s
RATED_WIND = 12.0             # m/s
CUT_OUT_WIND = 25.0            # m/s

# --- Rotor speed limits ---
MAX_RPM = 18.0                # RPM
MIN_RPM = 3.0                 # RPM

# --- Pitch angle limits ---
MIN_PITCH = 0.0               # degrees
MAX_PITCH = 25.0              # degrees

# --- Power coefficient limits ---
CP_MAX = 0.59                 # Betz limit
CP_NOMINAL = 0.45             # typical operating Cp

# --- Temperature thresholds ---
GEN_TEMP_WARN = 85.0          # °C
GEN_TEMP_CRIT = 95.0          # °C

GB_TEMP_WARN = 90.0           # °C
GB_TEMP_CRIT = 100.0          # °C

# --- Vibration thresholds ---
VIB_WARN = 6.0                # mm/s RMS
VIB_CRIT = 10.0               # mm/s RMS
