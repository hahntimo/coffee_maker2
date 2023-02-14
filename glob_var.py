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

# --- processes ---
pump_process = None
heater_process = None
can_spinner_process = None
switch_process = None
switch_manager = None
switch_mp_data = None


# --- pins ---
PIN_SWITCH_SERVO = 13


# --- configuration JSON ---
config_json = None
default_config_json = {
    "settings": {
        "sound_on": True
    },
    "calibration": {
        "motor_pump": 0.0,
        "motor_spinner": 0.0,
        "servo_angle_heater": 160,
        "servo_angle_brewing": 55
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
