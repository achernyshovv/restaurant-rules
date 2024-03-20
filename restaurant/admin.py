from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cook, Dish, Ingredient, DishType


@admin.register(Cook)
class CookAdmin(UserAdmin):
    search_fields = ("first_name", "last_name")
    list_display = ("username", "first_name", "last_name", "years_of_experience")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "years_of_experience",
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["username"].disabled = False
        return form


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name", "price")
    list_display = (
        "name",
        "price",
        "dish_type",
        "get_cooks_list",
        "get_ingredients_list",
    )
    list_filter = ("dish_type", "cooks", "ingredients")
    filter_horizontal = ("ingredients",)

    def get_cooks_list(self, obj):
        return ", ".join([cook.username for cook in obj.cooks.all()])

    get_cooks_list.short_description = "Cooks"

    def get_ingredients_list(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])

    get_ingredients_list.short_description = "Ingredients"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
