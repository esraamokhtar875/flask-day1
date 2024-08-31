
from flask import Flask,  url_for, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/index")
def index():
    posts=Post.query.all()
    return render_template("/index.html", posts=posts)

@app.route("/posts/<int:id>", endpoint="show")
def show(id):
    post=Post.query.get_or_404(id)
    return render_template("/show.html", post=post)



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description= db.Column(db.String(300))
    image = db.Column(db.String(200))


@app.route("/create", endpoint="create", methods=["GET","POST" ])
def create():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        image =  request.form['image']
        post= Post (name=name, description=description, image=image)
        db.session.add (post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("create.html")

@app.route("/Delete/<int:id>", endpoint="delete")
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/edit/<int:id>',methods=["GET","POST"], endpoint='edit_post')
def edit(id):
    post= Post.query.get_or_404(id)
    if request.method == 'POST':
        post.name = request.form.get('name')
        post.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)



if __name__ == '__main__':
    app.run(debug=True)









