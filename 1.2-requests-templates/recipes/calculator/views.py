from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def recipe_view(request, dish):
    recipe = DATA.get(dish, {})

    servings_raw = request.GET.get('servings', 1)
    try:
        servings = int(servings_raw)
        if servings <= 0:
            servings = 1
    except (TypeError, ValueError):
        servings = 1

    recipe_for_servings = {
        ingredient: round(amount * servings, 2)
        for ingredient, amount in recipe.items()
    }

    context = {
        'recipe': recipe_for_servings,
    }

    return render(request, 'calculator/index.html', context)
