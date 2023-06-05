from django import forms
from .models import Task
from .models import Cumple
from .models import *
from django import forms
import datetime
from datetime import date
from django.core.exceptions import ValidationError 



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Escriba un titulo'}),
             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Escriba una descripcion'}),
              'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
        

    
class CumpleForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Fecha', 'class': 'form-control','type': 'date'}),
        #help_text='Formato: DD/MM/AAAA'
    )
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cumpleañero', 'class': 'form-control'}),
        
    )
    def clean_fecha(self):
        data = self.cleaned_data["fecha"]

        fecha = date.today() 
        
        data_str = data.strftime('%d/%m/%Y')
        data_nueva = datetime.datetime.strptime(data_str, '%d/%m/%Y').date()
        
        if data_nueva > fecha:
            raise ValidationError("Fecha invalida")
        return data
    
    class Meta:
        model = Cumple
        fields = ('fecha', 'descripcion')

        