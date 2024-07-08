import os

from flask import current_app


class RecipeRepository:
    @staticmethod
    def find_all():
        path = os.path.join(current_app.instance_path, 'recipes.txt')

        with open(path, encoding='utf-8') as file:
            recipes = []

            file.readline()  # header

            for line in file:
                recipe = Recipe.create_from_line(line)
                recipes.append(recipe)

            return recipes

    @staticmethod
    def find_by_id(recipe_id):
        for recipe in RecipeRepository.find_all():
            if recipe.id == recipe_id:
                return recipe

        return None

    @staticmethod
    def find_all_by_name_like(name):
        return [
            recipe
            for recipe in RecipeRepository.find_all()
            if name.lower() in recipe.name.lower()
        ]

    @staticmethod
    def save(recipe):
        recipes = RecipeRepository.find_all()

        if not recipe.id:
            max_id = 0

            for i in range(len(recipes)):
                if recipes[i].id > max_id:
                    max_id = recipes[i].id

            recipe.id = max_id + 1
            recipes.append(recipe)
        else:
            for i in range(len(recipes)):
                if recipes[i].id == recipe.id:
                    recipes[i] = recipe
                    break

        RecipeRepository.__store_all(recipes)

        return recipe

    @staticmethod
    def delete(recipe):
        recipes = RecipeRepository.find_all()

        for i in range(len(recipes)):
            if recipes[i].id == recipe.id:
                recipes.pop(i)
                break

        RecipeRepository.__store_all(recipes)

    @staticmethod
    def __store_all(recipes):
        path = os.path.join(current_app.instance_path, 'recipes.txt')

        with open(path, 'w', encoding='utf-8') as file:
            file.write('id\tcategory\tname\tdifficulty\n')

            for recipe in sorted(recipes, key=lambda item: f'{item.category}\0{item.name}'):
                file.write(f'{recipe.to_line()}\n')


from models import Recipe
