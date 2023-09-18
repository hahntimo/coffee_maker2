"""Includes all global variables"""

# --- menu frames ---
boot_frame = None
main_menu_frame = None

# main menu
brewing_frame = None
profile_frame = None
test_frame = None
settings_frame = None

# test menu
pump_menu_frame = None
heater_menu_frame = None
can_spinner_menu_frame = None
switch_menu_frame = None

# --- processes and mp manager data ---
pump_process = None
pump_task_queue = None
pump_mp_data = None

heater_process = None
heater_mp_data = None

spinner_process = None
spinner_task_queue = None
spinner_output_queue = None

relay_process = None
relay_mp_data = None

# --- pins ---
# relays
PIN_BREWER_VALVE_RELAY = 13
PIN_HEATER_VALVE_RELAY = 6
PIN_HEATER_RELAY = 5

# spinner
PIN_SPINNER_DIRECTION = 19
PIN_SPINNER_STEP = 26
PIN_SPINNER_MOTOR_1 = 16
PIN_SPINNER_MOTOR_2 = 20
PIN_SPINNER_MOTOR_3 = 21

# pump
PIN_PUMP_DIRECTION = 24
PIN_PUMP_STEP = 23
PIN_PUMP_MOTOR_1 = 14
PIN_PUMP_MOTOR_2 = 15
PIN_PUMP_MOTOR_3 = 18


# --- configuration JSON ---
config_json = None
default_config_json = {
    "settings": {
        "sound_on": True
    },
    "calibration": {
        "pump_step_delay": 0.0,
        "pump_ml_per_revolution": 5,
        "spinner_step_delay": 0.0
    },
    "profiles": {
        "Neues Profil": {"blooming_bool": True,
                         "blooming_duration": 30,
                         "blooming_amount_percent": 10.0,
                         "coffee_gr_per_500ml": 30.0,
                         "brew_speed_ml_per_minute": 200,
                         "brew_temperature_celsius": 92.0}
    }
}
