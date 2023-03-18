from django import forms


TYPE_CHOICES =(
    ("text", "text"),
    ("number", "number"),
)
class GenerateDummyForm(forms.Form):
    field_name_1 = forms.CharField(max_length=100,label="Field Name 1",)
    field_name_2 = forms.CharField(max_length=100,label="Field Name 2",)
    type_1 = forms.ChoiceField(choices = TYPE_CHOICES , label="Type",widget=forms.Select(attrs={'class': 'form-select form-control'}))
    type_2 = forms.ChoiceField(choices = TYPE_CHOICES , label="Type",widget=forms.Select(attrs={'class': 'form-select form-control'}))
