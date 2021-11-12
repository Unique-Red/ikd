from flask import render_template, session, request, redirect, url_for, flash
from sqlalchemy.sql.functions import current_user
from .models import Post, User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website import app, db
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
@app.route("/home")
def home():
    return render_template ("home.html")

@app.route("/dig")
def dignitaries():
    return render_template ("dig.html")

@app.route("/a&g")
def ach():
    return render_template ("achievement.html")

@app.route("/about")
def about():
    return render_template ("about.html")

@app.route("/project")
def project():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template ("project.html", posts=posts)

'''@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        if request.form.get("username") == "Red" and request.form.get("password") == "red@123":
            session['logged_in'] = True
            return redirect("/create")
        else:
            return render_template("admin/auth.html", failed=True)
    return render_template ("admin/auth.html")'''

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('table'))
            else:
                flash("Password is incorrect", category='error') 
        else:
            flash("Username does not exist", category='error')

    return render_template ("admin/auth.html")


@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash("Username in use.", category='error') 
        elif password1 != password2:
            flash("Password don't match!", category='error') 
        elif len(username) < 2:
            flash("Username is too short", category='error') 
        elif len(password1) < 6:
            flash("Password is too short", category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('table'))


    return render_template ("admin/register.html")
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


'''@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")'''

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")
            file = request.files.get("file")

            if not text:
                return ('Details cannot be empty!')
            else:
                path = os.path.join("website", "static", "uploads", file.filename)
                post = Post(title=title, text=text, file=file.filename)
                file.save(path)
                
                db.session.add(post)
                db.session.commit()

                return redirect(url_for('project'))
    return render_template ("admin/create.html")

@app.route("/table", methods=["GET","POST"])
@login_required
def table():
    posts = Post.query.all()
    return render_template ("admin/table.html", posts=posts)

@app.route("/title", methods=["GET","POST"])
@login_required
def title():
    posts = Post.query.all()
    return render_template ("admin/title.html", posts=posts)

@app.route("/text", methods=["GET","POST"])
@login_required
def text():
    posts = Post.query.all()
    return render_template ("admin/text.html", posts=posts)

@app.route("/file", methods=["GET","POST"])
@login_required
def file():
    posts = Post.query.all()
    return render_template ("admin/files.html", posts=posts)



@app.route("/updatetitle/<int:id>", methods=['GET','POST'])
@login_required
def updatetitle(id):
    title_to_update = Post.query.get_or_404(id)
    if request.method=="POST":
        title_to_update.title = request.form['title']
        try:
            db.session.commit()
            return redirect('/title')

        except:
            flash("There was a problem updating this title")
    else:
        return render_template("admin/updatetitle.html", title_to_update=title_to_update)



@app.route("/updatetext/<int:id>", methods=["GET","POST"])
@login_required
def updatetext(id):
    text_to_update = Post.query.get_or_404(id)
    if request.method=="POST":
        text_to_update.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/text')

        except:
            flash("There was a problem updating this project")
    else:
        return render_template("admin/updatetext.html", text_to_update=text_to_update)


@app.route("/updatetable/<int:id>", methods=["GET","POST"])
@login_required
def updatetable(id):
    posts = Post.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get("title")
        text = request.form.get("text")
        file = request.files["file"]
        posts.title = title
        posts.text = text
        file.save(os.path.join(os.path.abspath(__package__),"static/uploads/"+file.filename))
        posts.file = file.filename
        flash("Edited Successfully!", "Success")
        db.session.commit()
    return render_template("admin/updatetable.html", posts=posts)

@app.route("/updatefile/<int:id>", methods=['GET','POST'])
@login_required
def updatefile(id):
    posts = Post.query.get_or_404(id)
    if request.method=="POST":
        posts.file = request.files['file']
        file.save(os.path.join(os.path.abspath(__package__),"static/uploads/"+file.filename))
        posts.file = file.filename
        try:
            db.session.commit()
            return redirect('/file')

        except:
            flash("There was a problem updating this file")
    else:
        return render_template("admin/updatefile.html", posts=posts)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    project_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(project_delete)
        db.session.commit()
        return redirect("/table")

    except:
        flash("There was a problem deleting this project", category='error')