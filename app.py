from flask import Flask, render_template

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "<p>Health Check OK!</p>"

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/graph")
def graph():
    return render_template("graph.html")

@app.route("/search", methods=["POST"])
def search():
    data: dict = request.get_json() 
    if not data: 
        return jsonify({"error": "No data provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)