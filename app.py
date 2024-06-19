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
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            border: 1px solid #e3e3e3;
        }

        h1 {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 5px;
            color: #666;
            font-size: 14px;
        }

        input[type="text"],
        input[type="email"] {
            padding: 12px;
            margin-bottom: 15px;
            border: 1px solid #d1d1d1;
            border-radius: 6px;
            font-size: 16px;
            background-color: #fdfdff;
        }

        input[type="text"]:focus,
        input[type="email"]:focus {
            border-color: #b6b6b6;
            outline: none;
        }

        button {
            padding: 12px;
            background-color: #8e8e8e;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #6d6d6d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sign Up for Legislative Updates</h1>
        <form id="signup-form">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            
            <label for="zip">ZIP Code:</label>
            <input type="text" id="zip" name="zip" required>
            
            <button type="submit">Sign Up</button>
        </form>
    </div>

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
