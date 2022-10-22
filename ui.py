from flask import Flask, render_template, url_for, request
app = Flask(__name__, template_folder="app_templates")
@app.route("/application", methods=["POST", "GET"])
def index():
    if request.method == 'POST' or request.method == 'GET':
        print(request.form)
    return render_template('ui.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)
