from django import models
from .states import INDIAN_STATES

class StateField(models.CharField):
	def __init__(self,*args,**kwargs):
		kwargs["max_length"] = 2 #use state code
		kwargs["choices"] = INDAN_STATES
		super().__init__(*args,**kwargs)