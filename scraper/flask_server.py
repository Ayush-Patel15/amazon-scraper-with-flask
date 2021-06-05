# Imports
from flask import Flask, json, jsonify, request, render_template
from werkzeug.datastructures import RequestCacheControl
from amazon_scraper import get_links, get_details
from concurrent.futures import ThreadPoolExecutor

# Initializing the app
app = Flask(__name__)

# Route for home page
@app.route("/")
def home():
    return render_template("home.html")

# search path
@app.route("/search",methods=["GET","POST"])
def search():
    try:
        # With search bar present in page or "home.html"
        query = request.form.get("search")
        if query:
            data = []
            page = 1
            links = get_links(query,page)
            with ThreadPoolExecutor() as executor:
                results = executor.map(get_details,links)
            for result in results:
                data.append(result)
            return jsonify(data)
        else:
            data = []
            # with chrome address bar
            query = request.args["query"]
            page = request.args["page"]
            links = get_links(query,page)
            with ThreadPoolExecutor() as executor:
                results = executor.map(get_details,links)
            for result in results:
                data.append(result)
            return jsonify(data)

    except Exception as e:
        return jsonify({
            "status": "Failed",
            "msg":"try for any other query please!!",
            "exception": e
        })


if __name__ == "__main__":
    app.run(debug=True,port=8000)
