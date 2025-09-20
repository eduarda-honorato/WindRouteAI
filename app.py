from flask import Flask

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "<p>Health Check OK!</p>"

@app.route("/")
def home():
    return "<h1>Welcome to WindRouteAI!</h1><p>Your solution for wind route optimization.</p>"

@app.route("/about")
def about():
    return "<h1>About WindRouteAI</h1><p>This application provides wind route optimization services.</p>"

@app.route("/graph")
def graph():
    return "<h1>Graph Page</h1><p>Graph-related functionalities will be implemented here.</p>"

@app.route("/search")
def search():
    return "<h1>Search Page</h1><p>Search-related functionalities will be implemented here.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)