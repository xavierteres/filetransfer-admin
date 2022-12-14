from flask import Flask, render_template, request, redirect, url_for
import utils.db as db
import os, in_place
import shutil

app = Flask(__name__)


@app.route("/")
def index():
    users = db.get_users()
    return render_template("index.html", users=users)


@app.route("/delete", methods=["POST"])
def delete():
    username = request.json["username"]
    user = db.get_user(username)
    if user:
        if db.remove_user(username) > 0:
            # Remove user credentials
            os.system("htpasswd -D /etc/nginx/.htpasswd " + username)
            # Update Nginx configuration file
            with in_place.InPlace("/etc/nginx/nginx.conf") as file:
                for line in file:
                    if " {} ".format(username) not in line:
                        file.write(line)
            # Reload Nginx
            os.system("systemctl reload nginx")
            return "Success"
    return "Fail"


@app.route("/switchPlan", methods=["POST"])
def switch_plan():
    username = request.json["username"]
    user = db.get_user(username)
    if user:
        if db.update_plan(username, not user[2]) > 0:
            # Update Nginx configuration file
            with in_place.InPlace("/etc/nginx/nginx.conf") as file:
                port = "3500" if not user[2] else "3000"
                for line in file:
                    if " {} ".format(username) in line:
                        file.write("        " + username + " " + port + ";\n")
                    else:
                        file.write(line)
            # Reload Nginx
            os.system("systemctl reload nginx")
            return "Success"
    return "Fail"


@app.route("/updatePassword", methods=["POST"])
def update_password():
    username = request.json["username"]
    new_password = request.json["password"]
    user = db.get_user(username)
    if user:
        # Create user credentials
        os.system("htpasswd -b /etc/nginx/.htpasswd " + username + " " + new_password)
        # Reload Nginx
        os.system("systemctl reload nginx")
        return "Success"
    return "Fail"


@app.route("/users", methods=["POST"])
def users():
    username = request.form["username"]
    password = request.form["password"]
    try:
        paid = request.form["paid"]
    except:
        paid = 0
    user = db.get_user(username)
    if not user:
        # Add user to db
        db.insert_user(username, paid)
        # Create user credentials
        os.system("htpasswd -b /etc/nginx/.htpasswd " + username + " " + password)
        # Add to Nginx configuration file
        with in_place.InPlace("/etc/nginx/nginx.conf") as file:
            port = "3500" if paid == "1" else "3000"
            for line in file:
                if "map $remote_user $target_port" in line:
                    file.write(line + "        " + username + " " + port + ";\n")
                else:
                    file.write(line)
        # Reload Nginx
        os.system("systemctl reload nginx")
    return redirect(url_for("index"))


@app.route("/newUpload", methods=["POST"])
def newUpload():
    sid = request.json["metadata"]["sid"]
    removeKey = request.json["metadata"]["removeKey"]

    upload = db.get_upload(sid)
    if not upload:
        # Add user to db
        db.insert_upload(sid, removeKey)
        return "True"
    else:
        return "False"


@app.route("/deleteUpload", methods=["GET"])
def deleteUpload():
    return render_template("delete.html")


@app.route("/removeUpload", methods=["POST"])
def removeUpload():
    sid = request.form["username"]
    removeKey = request.form["password"]

    upload = db.get_upload(sid)
    if upload:
        print(upload[2])
        if removeKey == upload[2]:
            db.remove_upload(sid)
            # Check if directory exists
            dir_path = "/root/data/" + sid
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
            return "Upload deleted"
        else:
            return "Incorrect delete key"

    return "Incorrect upload SID"
