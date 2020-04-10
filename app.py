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
@app.route("/", methods=["GET","POST"])
def index():
    return "Welcome to our shop!"


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
    my_username = request.form["user"]
    
    #curl
    curl = mysql.connection.cursor()
    curl.execute("SELECT * from users where username=(%s)",(my_username,))

    #commit
    mysql.connection.commit()

    data = curl.fetchall()


    curl.close()

    objeto_usuario = data

    if objeto_usuario and check_password_hash(objeto_usuario[0][2],request.form["password"]):
        #creamos la sesion
        session["username"] = objeto_usuario[0][1]


        return render_template("index.html", user=data[0])

    return redirect(url_for("login"))

@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop("username",None) #pasamos none para evitar errores

    return "You are logged out"

@app.route("/add_products",methods=["GET","POST"])
def add_products():
    return render_template("add_products.html")


@app.route("/shopping", methods=["GET","POST"])
def adding():
    if(request.method == "POST"):

        product = request.form["product"]
        units = request.form["units"]
        color = request.form["color"] 

        #curl

        curl = mysql.connection.cursor()
        curl.execute("INSERT INTO products (product, units, color) VALUES (%s, %s, %s)",
        (product, units, color))

        #commit
        mysql.connection.commit()

        curl.close()

        #mensaje entre vistas
        flash("product added succesfully", "success")

        return render_template("index.html")

@app.route("/cart", methods=["GET", "POST"])
def cart():

        #curl
        curl = mysql.connection.cursor()
        curl.execute("SELECT * from products")

        #commit
        mysql.connection.commit()

        data = curl.fetchall()

        curl.close()

        flash("mostrando carrito.. ", "success")

        return render_template("add_products.html", products=data[0])

if __name__ == "__main__":
    app.run(debug=True)