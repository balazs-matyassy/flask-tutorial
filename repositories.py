import os

import pymysql
from flask import current_app


def _get_connection():
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        port=current_app.config['DB_PORT'],
        user=current_app.config['DB_USERNAME'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor
    )


class RecipeRepository:
    @staticmethod
    def find_all():
        with _get_connection() as db:
            with db.cursor() as cursor:
                query = '''
                    SELECT `id`, `category`,`name`, `difficulty`
                    FROM `recipe`
                    ORDER BY `category`, `name`;
                '''

                cursor.execute(query)

                return [Recipe.create_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def find_by_id(recipe_id):
        with _get_connection() as db:
            with db.cursor() as cursor:
                query = '''
                    SELECT `id`, `category`,`name`, `difficulty`
                    FROM `recipe`
                    WHERE `id` = %s;
                '''
                args = (recipe_id,)

                cursor.execute(query, args)

                return Recipe.create_from_row(cursor.fetchone())

    @staticmethod
    def find_all_by_name_like(name):
        with _get_connection() as db:
            with db.cursor() as cursor:
                query = '''
                        SELECT `id`, `category`,`name`, `difficulty`
                        FROM `recipe`
                        WHERE `name` LIKE %s
                        ORDER BY `category`, `name`;
                    '''
                args = (f'%{name}%',)
                cursor.execute(query, args)

                return [Recipe.create_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def save(recipe):
        with _get_connection() as db:
            with db.cursor() as cursor:
                if not recipe.id:
                    query = '''
                        INSERT INTO `recipe`
                            (`category`, `name`, `difficulty`)
                        VALUES(%s, %s, %s);
                    '''
                    args = (
                        recipe.category,
                        recipe.name,
                        recipe.difficulty
                    )

                    cursor.execute(query, args)
                    db.commit()

                    recipe.id = cursor.lastrowid
                else:
                    query = '''
                        UPDATE `recipe`
                        SET `category` = %s,
                            `name` = %s,
                            `difficulty` = %s
                        WHERE `id` = %s;
                    '''
                    args = (
                        recipe.category,
                        recipe.name,
                        recipe.difficulty,
                        recipe.id
                    )

                    cursor.execute(query, args)
                    db.commit()

            return recipe

    @staticmethod
    def delete(recipe):
        with _get_connection() as db:
            with db.cursor() as cursor:
                query = '''
                    DELETE FROM `recipe`
                    WHERE `id` = %s;
                '''
                args = (recipe.id,)

                cursor.execute(query, args)
                db.commit()


from models import Recipe
