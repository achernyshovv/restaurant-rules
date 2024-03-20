from django import forms
from .models import Dish, Ingredient


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "dish_type", "ingredients", "cooks"]
        widgets = {
            "ingredients": forms.CheckboxSelectMultiple,
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        elif price >= 1001:
            raise forms.ValidationError("Price must be less than 1001.")
        return price

    def clean_experience(self):
        experience = self.cleaned_data["experience"]
        if experience <= 0:
            raise forms.ValidationError("Experience must be greater than zero")
        elif experience <= 5:
            raise forms.ValidationError("You can't create dish,"
                                        " your experience must be greater than 5"
                                        )
        elif experience >= 50:
            raise forms.ValidationError("Not valid experience."
                                        " We haven't cooks with more than 50 years experience"
                                        )
