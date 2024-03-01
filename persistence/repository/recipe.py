from persistence.repository import AbstractRepository
from persistence.utils import fetchall, fetchone, execute


class RecipeRepository(AbstractRepository):
    @staticmethod
    def find_all():
        query = '''
                SELECT `id`, `category`,`name`, `description`, `difficulty`
                FROM `recipe`
                ORDER BY `category`, `name`;
        '''

        return [Recipe.create(data) for data in fetchall(query)]

    @staticmethod
    def find_by_id(recipe_id):
        query = '''
                SELECT `id`, `category`, `name`, `description`, `difficulty`
                FROM `recipe`
                WHERE `id` = %s;
        '''
        args = (recipe_id,)

        return Recipe.create(fetchone(query, args))

    @staticmethod
    def find_all_by_name_like(name):
        query = '''
                SELECT `id`, `category`, `name`, `description`, `difficulty`
                FROM `recipe`
                WHERE `name` LIKE %s
                ORDER BY `category`, `name`;
        '''
        args = (f'%{name}%',)

        return [Recipe.create(data) for data in fetchall(query, args)]

    @staticmethod
    def save(recipe):
        if not recipe.id:
            query = '''
                    INSERT INTO `recipe`
                        (`category`, `name`, `description`, `difficulty`)
                    VALUES(%s, %s, %s, %s);
            '''
            args = (
                recipe.category,
                recipe.name,
                recipe.description,
                recipe.difficulty
            )
            recipe.id = execute(query, args)
        else:
            query = '''
                    UPDATE `recipe`
                    SET `category` = %s,
                        `name` = %s,
                        `description` = %s,
                        `difficulty` = %s
                    WHERE `id` = %s;
            '''
            args = (
                recipe.category,
                recipe.name,
                recipe.description,
                recipe.difficulty,
                recipe.id
            )
            execute(query, args)

        return recipe

    @staticmethod
    def delete_by_id(recipe_id):
        query = '''
                DELETE FROM `recipe`
                WHERE `id` = %s;
        '''
        args = (recipe_id,)
        execute(query, args)


from persistence.model.recipe import Recipe
