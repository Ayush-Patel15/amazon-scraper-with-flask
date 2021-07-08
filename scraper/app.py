# Imports
from flask import Flask, jsonify, request, render_template
from amazon_scraper import get_links, get_details
from best_deals import main_deals
from concurrent.futures import ThreadPoolExecutor

# Initializing the app
app = Flask(__name__)

# Route for home page
@app.route("/")
def home():
    urls = ["https://www.amazon.in"]
    deals = main_deals()
    return render_template("home.html", content=deals, url=urls)

# search path
@app.route("/search",methods=["GET","POST"])
def search():
    try:
        # With search bar present in page or "home.html"
        query = request.form.get("search")
        page = request.form.get("pages")
        if query:
            data = []
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
    app.run(debug=True)
