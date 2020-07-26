from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # three forward slashes for relative path (no need to specify an exact location)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # references id (of type Integer) of each task entry
    content = db.Column(db.String(200), nullable=False)  # holds task entry (of type String, max 200 characters) which cannot be null
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # sets date to every added task entry

    def __repr__(self):
        """returns a string every time we create a new element using task's id"""
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """routes to main to-do-list page, which accepts two methods: POST and GET"""
    if request.method == 'POST':
        task_content = request.form['content']  # represents contents from submitted form
        new_task = Todo(content=task_content)  # creates model based on contents from form

        try:
            db.session.add(new_task)
            db.session.commit()  # adds task entry to database
            return redirect('/')  # after update, redirect back to homepage to see new task
        except:
            return 'There was an issue adding your task'  # if there ever is a complication, this String will be returned

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # looks at database contents in order of date created and returns all of them
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')  # uses unique id to delete task
def delete(id):
    """removes task from database by unique id"""
    task_to_delete = Todo.query.get_or_404(id)  # attempts to get task by id; if id does not exist, will display 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()  # deletes task from database
        return redirect('/')  # after deletion, redirect back to homepage
    except:
        return 'There was an issue deleting your task'  # if there ever is a complication, this String will be returned


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """updates String content of specific task from database using submitted form"""
    task = Todo.query.get_or_404(id)  # attempts to get task by id; if id does not exist, will display 404

    if request.method == 'POST':
        task.content = request.form['content']  # updates the String content with new contents from the submitted form

        try:
            db.session.commit()  # no need to add or delete, just commit the updated content
            return redirect('/')  # after update, redirect back to homepage to see updated task
        except:
            return 'There was an issue updating your task'  # if there ever is a complication, this String will be returned

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
