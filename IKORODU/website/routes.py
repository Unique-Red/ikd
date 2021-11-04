from flask import render_template, session, request, redirect, url_for, flash
from sqlalchemy.sql.functions import current_user
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
    posts = Post.query.order_by(Post.date_created.desc()).all()
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

@app.route("/table", methods=["GET","POST"])
def table():
    posts = Post.query.all()
    return render_template ("admin/table.html", posts=posts)

@app.route("/title", methods=["GET","POST"])
def title():
    posts = Post.query.all()
    return render_template ("admin/title.html", posts=posts)

@app.route("/text", methods=["GET","POST"])
def text():
    posts = Post.query.all()
    return render_template ("admin/text.html", posts=posts)

@app.route("/updatetitle/<int:id>", methods=['GET','POST'])
def updatetitle(id):
    updatetitle = Post.query.get(id)
    title = request.form.get("title")
    if request.method=="POST":
        updatetitle.title = title
        flash(f"Your project has been updated","success")
        db.session.commit()
        return redirect(url_for("title"))
    return render_template("admin/updatetitle.html", updatetitle=updatetitle)



@app.route("/updatetext/<int:id>", methods=["GET","POST"])
def updatetext(id):
    updatetext = Post.query.get(id)
    text = request.form.get("text")
    if request.method=="POST":
        updatetext.text = text
        flash(f"Your project has been updated","success")
        db.session.commit()
        return redirect(url_for("text"))

    return render_template("admin/updatetext.html", updatetext=updatetext)

@app.route("/updatetable/<int:id>", methods=["GET","POST"])
def updatetable(id):
    posts = Post.query.get_or_404(id)
    title = request.form.get("title")
    text = request.form.get("text")
    text = request.form.get("text")
    date_created = request.form.get("date_created")
    return render_template("admin/updatetable.html", posts=posts, title=title)

