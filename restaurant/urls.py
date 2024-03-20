from django.urls import path

from .views import (
    index,
    DishListView,
    DishDetailView,
    dish_create,
    dish_update,
    dish_delete,
    IngredientListView,
    IngredientDetailView,
    DishTypeListView,
    CookListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", dish_create, name="dish-create"),
    path("dishes/<int:pk>/update/", dish_update, name="dish-update"),
    path("dishes/<int:pk>/delete/", dish_delete, name="dish-delete"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path(
        "ingredients/<int:pk>/",
        IngredientDetailView.as_view(),
        name="ingredient-detail",
    ),
    path("dishtypes/", DishTypeListView.as_view(), name="dish-type-list"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
]

app_name = "restaurant"
