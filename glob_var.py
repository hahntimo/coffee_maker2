config_json = None


# menu frames
boot_frame = None
main_menu_frame = None

brewing_frame = None
profile_frame = None
testing_frame = None
settings_frame = None


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
        "Reinigung": {"blooming_bool": True,
                      "blooming_duration": 30,
                      "coffee_gr_per_500ml": 31.5,
                      "brew_speed_ml_per_minute": 200}
    }
}