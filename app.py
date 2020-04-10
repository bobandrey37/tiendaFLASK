from flask import Flask, render_template, request, redirect, flash, make_response, session, escape, url_for
from flask_mysqldb import MySQL

#hashed pw
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#MySQL database connection 

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'tienda'

mysql = MySQL(app)

#settings 
app.secret_key = "mysecretkey" 

#routing
@app.route("/signup", methods=["GET","POST"])
def signup():
    
    if request.method == "POST":
        user = request.form["user"]
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        email = request.form["email"]

        #curl
        curl = mysql.connection.cursor()
        curl.execute("INSERT into users (username, password, email) VALUES (%s,%s,%s)",
        (user, hashed_pw,email))

        #commit
        mysql.connection.commit()

        #mensaje entre vistas
        flash("Genial! te has registrado.", "success")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/search",methods=["GET","POST"])
def search():
    return "Welcome user!"

if __name__ == "__main__":
    app.run(debug=True)