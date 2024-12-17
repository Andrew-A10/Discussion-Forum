from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)

# Home route displaying all posts
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# Route to create a new post
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('new_post.html')

# Route to view a specific post
@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    # Create database tables if they do not exist
    db.create_all()
    app.run(debug=True)
