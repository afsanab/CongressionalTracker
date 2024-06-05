from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    zip = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign Up</title>
    </head>
    <body>
        <h1>Sign Up for Legislative Updates</h1>
        <form id="signup-form">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            <br>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <br>
            <label for="zip">ZIP Code:</label>
            <input type="text" id="zip" name="zip" required>
            <br>
            <button type="submit">Sign Up</button>
        </form>

        <script>
            document.getElementById('signup-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const zip = document.getElementById('zip').value;

                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, email, zip })
                });

                if (response.ok) {
                    alert('Signed up successfully!');
                } else {
                    alert('Failed to sign up.');
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], zip=data['zip'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User signed up successfully"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
