from flask import render_template, session, request, redirect, url_for, g
from .models import Post
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
    posts = Post.query.all()
    return render_template ("project.html", posts=posts)

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        if request.form.get("username") == "Red" and request.form.get("password") == "red@123":
            session['logged_in'] = True
            return redirect("/create")
        else:
            return render_template("admin/auth.html", failed=True)
    return render_template ("admin/auth.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create", methods=['GET', 'POST'])
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


