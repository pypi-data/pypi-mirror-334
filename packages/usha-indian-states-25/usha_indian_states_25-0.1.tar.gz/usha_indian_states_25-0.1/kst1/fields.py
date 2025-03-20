from django.db import models
from .states import INDIAN_STATES  # Ensure the correct import path

class StateField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2  # State codes are usually 2 characters (like 'MH', 'UP')
        kwargs["choices"] = INDIAN_STATES  # Set the predefined choices
        super().__init__(*args, **kwargs)  # Properly call the parent class constructor
