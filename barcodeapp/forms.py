from django import forms

FOOD_CHOICES =(
    ("1", "Lunch"),
    ("2", "Dinner")
)

FOOD_CHOICES_DASHBOARD =(
    ("1", "Lunch"),
    ("2", "Dinner_veg"),
    ("3", "Dinner_nveg"),
    ("4", "Dinner_kid")
)

SERVICE_TYPE =(
    ("1", "Serviced"),
    ("2", "Not Services")
)

# creating a form
class DataForm(forms.Form):
    name_field = forms.CharField(required=True,label='Saikat Member Name',max_length = 500)
    email_field = forms.CharField(required=False,label='Saikat Member Email',max_length = 500)
    name1_field = forms.CharField(required=False,label='Saikat Member Name',max_length = 500)
    food_field = forms.ChoiceField(choices = FOOD_CHOICES)
    food_dash = forms.ChoiceField(choices = FOOD_CHOICES_DASHBOARD)
    service_type = forms.ChoiceField(choices = SERVICE_TYPE)
