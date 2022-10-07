from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, recipe


@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    all_recipes = recipe.Recipe.get_all_recipes()
    return render_template("recipes.html", logged_in_user=logged_in_user, recipes=all_recipes)

@app.route("/recipes/new")
def add_recipe_page():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template("add-recipe.html", logged_in_user = logged_in_user)

@app.route("/recipes/<int:id>")
def show_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    recipe_data = recipe.Recipe.get_recipe_by_id(id)
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template("show-recipe.html", logged_in_user = logged_in_user, recipe=recipe_data)

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    recipe_data = recipe.Recipe.get_recipe_by_id(id)
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template("edit-recipe.html", logged_in_user = logged_in_user, recipe=recipe_data)




@app.route("/recipes/create", methods=["POST"])
def add_new_recipe():
    if "user_id" not in session:
        return redirect('/')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    recipe.Recipe.add_new_recipe(request.form)
    return redirect("/recipes")


@app.route("/recipes/edit-recipe/<int:id>", methods=["POST"])
def update_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{id}")
    recipe.Recipe.update_recipe(request.form)
    return redirect("/recipes")

@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    recipe.Recipe.delete_recipe(id)
    return redirect("/recipes")
