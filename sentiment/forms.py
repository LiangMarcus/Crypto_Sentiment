from django import forms
from . models import CryptoData


class CryptoDataForm (forms.ModelForm):
    class Meta:
        model = CryptoData
        fields = '__all__' 

#???
class SearchForm (forms.Form):
    q = forms.CharField(label='Search', max_length=50)