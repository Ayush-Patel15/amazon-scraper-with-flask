from flask import Flask, jsonify, request, render_template
from amazon_scraper import get_links, get_details

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search.html")

@app.route("/search")
def search():
    query = request.args["query"]
    page = request.args["page"]
    links = get_links(query)
    if len(links) > 0:
        data = get_details(links,page)
        return jsonify(data)
    else:
        return jsonify({"status": "Failed","msg":"try for any other query please!!"})

if __name__ == "__main__":
    app.run(debug=True,port=8000)

