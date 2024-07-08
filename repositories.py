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
    def find_all_by_name_like(name):
        return [
            recipe
            for recipe in RecipeRepository.find_all()
            if name.lower() in recipe.name.lower()
        ]

    @staticmethod
    def find_by_id(recipe_id):
        for recipe in RecipeRepository.find_all():
            if recipe.id == recipe_id:
                return recipe

        return None


from models import Recipe
