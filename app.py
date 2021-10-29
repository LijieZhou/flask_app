import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?',
                        (recipe_id,)).fetchone()
    conn.close()
    if recipe is None:
        abort(404)
    return recipe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecurestring'

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/<int:recipe_id>')
def recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Boooo! Your beer needs a name!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO recipes (title, content) VALUES (?,?)',
                     (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:recipe_id>/edit', methods=('GET', 'POST'))
def edit(recipe_id):
    recipe = get_recipe(recipe_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Boooo! Your beer needs a name~')
        conn = get_db_connection()
        conn.execute('UPDATE recipes SET title = ?, content = ?' ' WHERE id = ?', (title, content, recipe_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', recipe=recipe)
