from flask import Flask, render_template, request, redirect, url_for
import utils.db as db
import os, in_place

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
            # TODO: Delete from Nginx config, password and restart
            return [user]
    return []


@app.route("/switchPlan", methods=["POST"])
def switch_plan():
    username = request.json["username"]
    user = db.get_user(username)
    if user:
        if db.update_plan(username, not user[2]) > 0:
            # TODO: Update from Nginx config and restart
            return [user]
    return []


@app.route("/updatePassword", methods=["POST"])
def update_password():
    username = request.json["username"]
    new_password = request.json["password"]
    user = db.get_user(username)
    if user:
        # TODO: Update password and restart
        print(new_password)
        return [user]
    return []


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
        os.system("htpasswd /etc/nginx/.htpasswd -m " + user + password)

        # Add to Nginx configuration file
        with in_place.InPlace('/etc/nginx/nginx.conf') as file:
            for line in file:
                port = "3500" if paid == 1 else "3000"
                if "map $remote_user $target_port" in line:
                    file.write(line + "        " + user + " " + port + "\n")
                else:
                    file.write(line)

        # Reload Nginx
        os.system("systemctl reload nginx")

    return redirect(url_for("index"))
