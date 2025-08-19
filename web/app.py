from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
mydb = client["routerdb"]
mycol = mydb["routers"]

sample = Flask(__name__)

@sample.route("/")
def main():
    data = list(mycol.find())
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        all_docs = list(mycol.find())
        if 0 <= idx < len(all_docs):
            mycol.delete_one({"_id": all_docs[idx]["_id"]})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)