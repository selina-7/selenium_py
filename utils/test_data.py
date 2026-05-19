USERS = {
    "standard":    {"username": "standard_user",             "password": "secret_sauce"},
    "locked":      {"username": "locked_out_user",            "password": "secret_sauce"},
    "problem":     {"username": "problem_user",               "password": "secret_sauce"},
    "perf_glitch": {"username": "performance_glitch_user",    "password": "secret_sauce"},
}

VALID_USERS = [
    ("standard_user",             "secret_sauce"),
    ("performance_glitch_user",   "secret_sauce"),
]

INVALID_USERS = [
    ("wrong_user",    "secret_sauce", "Epic sadface"),
    ("standard_user", "wrong_pass",   "Epic sadface"),
    ("",              "",             "Username is required"),
    ("standard_user", "",            "Password is required"),
]

PRODUCTS = {
    "backpack":   "Sauce Labs Backpack",
    "bike_light": "Sauce Labs Bike Light",
    "t_shirt":    "Sauce Labs Bolt T-Shirt",
    "fleece":     "Sauce Labs Fleece Jacket",
    "onesie":     "Sauce Labs Onesie",
    "ringer":     "Test.allTheThings() T-Shirt (Red)",
}

CHECKOUT_VALID = {"first_name": "Test", "last_name": "Kullanici", "postal_code": "01000"}
CHECKOUT_NO_FIRST = {"first_name": "", "last_name": "Kullanici", "postal_code": "01000"}
