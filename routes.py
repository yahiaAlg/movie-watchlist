from dataclasses import asdict
import datetime
from pprint import pprint
import uuid
from flask import Blueprint, current_app, render_template, redirect, url_for, flash
from .forms import MovieForm
from .models import Movie

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def home():
    movies = current_app.db.select("movies")
    return render_template("pages/home.html", movies=movies)

@pages.route("/movie/<movie_id>")
def movie_details(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        flash("Movie not found", "error")
        return redirect(url_for("pages.home"))
    return render_template("pages/details.html", movie=movie[0])

@pages.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        new_movie = Movie(
            _id=str(uuid.uuid4()),
            title=form.title.data,
            director=datetime.date.isoformat(form.year.data),
            year=form.year.data,
            description=form.description.data,
            tags=form.tags.data.split(",") if form.tags.data else [],
            casts=form.casts.data.split(",") if form.casts.data else [],
            series=form.series.data.split(",") if form.series.data else [],
            rating=form.rating.data,
            video_link=form.video_link.data
        )
        current_app.db.insert("movies", asdict(new_movie))
        flash("Movie added successfully", "success")
        return redirect(url_for("pages.home"))

    return render_template("pages/add_movie.html", form=form)

@pages.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        flash("Movie not found", "error")
        return redirect(url_for("pages.home"))

    movie = movie[0]  # Get the first (and only) result
    movie_obj = Movie(**movie)
    movie_obj.year = datetime.date.fromisoformat(movie_obj.year)
    form = MovieForm(obj=movie_obj)
    pprint(movie_obj)

    if form.validate_on_submit():
        updated_movie = Movie(
            _id=movie_id,
            title=form.title.data,
            director=form.director.data,
            year=datetime.date.isoformat(form.year.data),
            description=form.description.data,
            tags=form.tags.data.split(",") if form.tags.data else [],
            casts=form.casts.data.split(",") if form.casts.data else [],
            series=form.series.data.split(",") if form.series.data else [],
            rating=form.rating.data,
            video_link=form.video_link.data
        )

        current_app.db.update("movies", lambda x:x["_id"] == movie_id, lambda x: x.update(asdict(updated_movie)))
        flash("Movie updated successfully", "success")
        return redirect(url_for("pages.home"))

    return render_template("pages/edit_movie.html", form=form, movie_id=movie_id)

@pages.route("/delete_movie/<movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        flash("Movie not found", "error")
    else:
        current_app.db.delete("movies", movie_id)
        flash("Movie deleted successfully", "success")
    return redirect(url_for("pages.home"))