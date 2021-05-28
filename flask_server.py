from flask import Flask, jsonify, request
from amazon_scraper import get_links, get_details

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify("Hello, World!!")

@app.route("/search")
def search():
    query = request.args["query"]
    links = get_links(query)
    if len(links) > 0:
        data = get_details(links)
        return jsonify(data)
    else:
        return jsonify({"status": "Failed","msg":"try for any other query please!!"})

if __name__ == "__main__":
    app.run(debug=True,port=8000)

