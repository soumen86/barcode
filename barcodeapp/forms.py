from django import forms

FOOD_CHOICES =(
    ("1", "Lunch"),
    ("2", "Dinner")
)

# creating a form
class DataForm(forms.Form):
    name_field = forms.CharField(required=True,label='Saikat Member Name',max_length = 500)
    food_field = forms.ChoiceField(choices = FOOD_CHOICES)
