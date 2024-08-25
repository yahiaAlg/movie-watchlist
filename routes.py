from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app, abort
from forms import LoginForm, RegistrationForm, MovieForm, EditProfileForm
from models import User, Movie
from decorators import login_required, redirect_if_logged_in, owner_required
import uuid
import datetime
from dataclasses import asdict
from pprint import pprint

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
pages = Blueprint('pages', __name__, template_folder='templates', static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        users = current_app.db.select('users', conditions={'email': email})
        if users and User(**users[0]).check_password(password):
            session['user_id'] = users[0]['id']
            return redirect(url_for('auth.profile'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('accounts/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        users = current_app.db.select('users', conditions={'email': email})
        if users:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        new_user = User(email=email, name=name, password=password)
        new_user.set_password(password)
        current_app.db.insert('users', asdict(new_user))
        session['user_id'] = new_user.id
        return redirect(url_for("auth.login"))
    return render_template('accounts/register.html', form=form)

@auth.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    users = current_app.db.select('users', conditions={'id': user_id})
    user = users[0] if users else None
    return render_template('accounts/profile.html', user=user)

@pages.route("/")
@login_required
def home():
    user_id = session.get('user_id')
    user = current_app.db.select('users', conditions={'id': user_id})[0]
    movie_ids = user['movie_ids']
    movies = [Movie(**movie) for movie in current_app.db.select('movies') if movie['_id'] in movie_ids]
    return render_template("pages/home.html", movies=movies)

@pages.route("/movie/<movie_id>")
@login_required
@owner_required
def movie_details(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        abort(404)
    movie = Movie(**movie[0])
    movie.last_seen = datetime.datetime.fromisoformat(movie.last_seen).strftime("in %b %d at %H:%M")
    return render_template("pages/details.html", movie=movie)

@pages.route("/add_movie", methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm()
    user_id = session.get('user_id')

    if form.validate_on_submit():
        new_movie = Movie(
            _id=str(uuid.uuid4()),
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
        current_app.db.insert("movies", asdict(new_movie))
        current_app.db.update("users", lambda x: x['id'] == user_id, lambda x: x['movie_ids'].append(new_movie._id))
        flash("Movie added successfully", "success")
        return redirect(url_for("pages.home"))

    return render_template("pages/add_movie.html", form=form)

@pages.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
@login_required
@owner_required
def edit_movie(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        abort(404)
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

        current_app.db.update("movies", lambda x: x["_id"] == movie_id, lambda x: x.update(asdict(updated_movie)))
        flash("Movie updated successfully", "success")
        return redirect(url_for("pages.home"))

    return render_template("pages/edit_movie.html", form=form, movie_id=movie_id)

@pages.route("/delete_movie/<movie_id>", methods=["POST"])
@login_required
@owner_required
def delete_movie(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    if not movie:
        flash("Movie not found", "error")
    else:
        current_app.db.delete("movies", lambda x: x["_id"] == movie_id)
        current_app.db.update("users", lambda x: movie_id in x['movie_ids'], lambda x: x['movie_ids'].remove(movie_id))
        flash("Movie deleted successfully", "success")
    return redirect(url_for("pages.home"))

@pages.route("/change_last_seen/<movie_id>", methods=["POST"])
@login_required
@owner_required
def change_last_seen(movie_id):
    movie = current_app.db.select("movies", conditions={"_id": movie_id})
    movie = Movie(**movie[0])
    if not movie:
        abort(404)
    else:
        pprint(movie)
        movie.last_seen = datetime.datetime.now().isoformat()
        current_app.db.update("movies", lambda x: x["_id"] == movie_id, lambda x: x.update(asdict(movie)))
        flash("Movie last seen date updated successfully", "success")
    return redirect(url_for("pages.home"))

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = current_app.db.select('users', conditions={'id': user_id})[0]
    user = User(**user)
    
    pprint(user)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        pprint(user)
        current_app.db.update('users', lambda x: x['id'] == user_id, lambda x: x.update(asdict(user)))
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('accounts/edit_profile.html', form=form)

# creating errors blueprint

def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500