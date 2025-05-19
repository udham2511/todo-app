from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# configuring database (SQLite)
baseDir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(baseDir, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"


# home route - shows all tasks
@app.route("/")
def index():
    tasks = Task.query.all()

    return render_template("index.html", tasks=tasks)


# add new task
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")

    if title:
        new_task = Task(title=title)

        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("index"))


# mark task as done
@app.route("/done/<int:id>")
def done(id):
    task = Task.query.get_or_404(id)

    task.is_done = not task.is_done

    db.session.commit()

    return redirect(url_for("index"))


# delete task
@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
