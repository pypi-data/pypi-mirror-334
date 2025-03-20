from django import forms
from .states import INDIAN_STATES

class StateSelect(forms.Select):
	def__init__(self,attrs=None):
		super().init__(attrs,choices=INDIAN_STATES)