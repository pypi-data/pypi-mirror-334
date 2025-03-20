from django import forms
from .states import INDIAN_STATES  # Ensure states.py exists and is correctly referenced

class StateSelect(forms.Select):  # Fixed typo: "form.Select" → "forms.Select"
    def __init__(self, attrs=None):
        super().__init__(attrs, choices=INDIAN_STATES)  # Fixed "choice" → "choices"
