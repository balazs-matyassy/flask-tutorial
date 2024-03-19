import pymysql
from flask import Flask, render_template, abort, request

from recipe import Recipe

app = Flask(__name__)


@app.route('/')
def dict_recipes():
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='cookbook_tutorial',
        cursorclass=pymysql.cursors.DictCursor
    )

    with db:
        with db.cursor() as cursor:
            query = '''
                    SELECT `id`, `category`,`name`, `difficulty`
                    FROM `recipe`
                    ORDER BY `category`, `name`;
            '''

            cursor.execute(query)

            recipes = cursor.fetchall()

    return render_template('list.html', recipes=recipes, title='DICT')


@app.route('/obj')
def obj_recipes():
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='cookbook_tutorial',
        cursorclass=pymysql.cursors.DictCursor
    )

    with db:
        with db.cursor() as cursor:
            query = '''
                    SELECT `id`, `category`,`name`, `difficulty`
                    FROM `recipe`
                    ORDER BY `category`, `name`;
            '''

            cursor.execute(query)

            recipes = [Recipe.create(data) for data in cursor.fetchall()]

    return render_template('list.html', recipes=recipes, title='OBJ')


if __name__ == '__main__':
    app.run()
