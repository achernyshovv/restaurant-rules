from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Dish, Ingredient, DishType, Cook
from .forms import DishForm


def index(request: HttpRequest) -> HttpResponse:
    num_ingredients = Ingredient.objects.count()
    num_dish = Dish.objects.count()
    num_dish_type = DishType.objects.count()
    num_cooks = Cook.objects.count()
    context = {
        "num_ingredients": num_ingredients,
        "num_dish": num_dish,
        "num_dish_type": num_dish_type,
        "num_cooks": num_cooks,
    }

    return render(request, "restaurant/index.html", context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "restaurant/cook_list.html"
    context_object_name = "cooks"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "restaurant/dish_list.html"
    context_object_name = "dishes"

    def get_queryset(self, *args, **kwargs):
        return Dish.objects.filter(cooks=self.request.user)


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "restaurant/dish_detail.html"
    context_object_name = "dish"

    def get_queryset(self):
        return super().get_queryset().filter(cooks=self.request.user)


@login_required
def dish_create(request):
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.save()
            cook, created = Cook.objects.get_or_create(username=request.user.username)
            dish.cooks.add(cook)
            dish.save()
            return redirect("restaurant:dish-detail", pk=dish.pk)
    else:
        form = DishForm()
    return render(request, "restaurant/dish_form.html", {"form": form})


@login_required
def dish_update(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == "POST":
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            dish = form.save()
            messages.success(request, "Dish updated successfully!")
            return redirect("restaurant:dish-detail", pk=dish.pk)
    else:
        form = DishForm(instance=dish)

    return render(request, "restaurant/dish_form.html", {"form": form})


@login_required
def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == "POST":
        dish.delete()
        messages.success(request, "Dish deleted successfully!")
        return redirect("restaurant:dish-list")

    return render(request, "restaurant/dish_confirm_delete.html", {"dish": dish})


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "restaurant/ingredient_list.html"
    context_object_name = "ingredients"


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    template_name = "restaurant/ingredient_detail.html"
    context_object_name = "ingredient"


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "restaurant/dish_type_list.html"
    context_object_name = "dish_type"
