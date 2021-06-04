from flask import Flask, json, jsonify, request, render_template
from amazon_scraper import get_links, get_details

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search",methods=["GET","POST"])
def search():
    try:
        query = request.form.get("search")
        if query:
            page = 1
            links = get_links(query)
            if len(links) > 0:
                data = get_details(links,page)
                return jsonify(data)
        else:
            query = request.args["query"]
            page = request.args["page"]
            links = get_links(query)
            if len(links) > 0:
                data = get_details(links,page)
                return jsonify(data)
    except Exception as e:
        return jsonify({
            "status": "Failed",
            "msg":"try for any other query please!!",
            "exception": e
            })
                
# todo: Error handling


if __name__ == "__main__":
    app.run(debug=True,port=8000)
