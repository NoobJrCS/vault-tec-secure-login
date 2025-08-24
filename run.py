# run.py

from flask import Flask, render_template

# Basic App Initialization
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# A temporary route to display the registration page
@app.route('/')
def register():
    """Renders the registration page."""
    return render_template('register.html')

# This is required to run the app
if __name__ == '__main__':
    app.run(debug=True)