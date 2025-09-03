from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
import os

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]
interface_col = mydb["interface_status"]

sample = Flask(__name__)


@sample.route("/")
def main():
    data = list(mycol.find())
    return render_template("index.html", data=data)


@sample.route("/router/<router_ip>")
def router_detail(router_ip):
    router_data = list(interface_col.find({"router_ip": router_ip}))
    return render_template("router_detail.html", data=router_data, ip=router_ip)


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
