from flask import Flask, render_template, request, redirect, flash, make_response, session, escape, url_for
from flask_mysqldb import MySQL

#hashed pw
from werkzeug.security import generate_password_hash, check_password_hash

#initializations
app = Flask(__name__)

#MySQL database connection 

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'tienda'

mysql = MySQL(app)

#settings 
app.secret_key = 'mysecretkey'

#routing
@app.route('/', methods=['GET','POST'])
def index():
    return 'Welcome to our shop!'


@app.route('/show', methods=['GET','POST'])
def show():
    curl = mysql.connection.cursor()
    curl.execute('SELECT * from products')
    data = curl.fetchall()

    return render_template("add_products.html", products = data)

@app.route('/signup', methods=['GET','POST'])
def signup():
    
    if request.method == 'POST':
            user = request.form["user"]
            hashed_pw = generate_password_hash(request.form["password"], method="sha256")
            email = request.form["email"]

            #curl
            curl = mysql.connection.cursor()
            curl.execute("INSERT INTO users (username, password, email) VALUES (%s,%s,%s)",
            (user, hashed_pw,email))

            #commit
            mysql.connection.commit()

            #mensaje entre vistas
            flash('Flawless! you have just been registered','success')

            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/search',methods=['GET','POST'])
def search():
    my_username = request.form['user']
    
    #curl
    curl = mysql.connection.cursor()
    curl.execute('SELECT * from users where username=(%s)',(my_username,))

    #commit
    mysql.connection.commit()

    data = curl.fetchall()


    curl.close()

    objeto_usuario = data

    if objeto_usuario and check_password_hash(objeto_usuario[0][2],request.form['password']):
        #creamos la sesion
        session['username'] = objeto_usuario[0][1]

        return render_template("index.html",user=objeto_usuario[0][1])

    flash('user not found','error')
    return redirect(url_for('signup'))



@app.route('/logout', methods=["GET","POST"])
def logout():

    session.pop('username',None) #pasamos none para evitar errores

    return redirect(url_for('index'))

@app.route('/home', methods=['GET','POST'])
def home():

    if request.method == 'POST':

        if 'username' in session:

            return render_template('index.html')

    flash('You must log in first to access shopping page!','error')
    return redirect(url_for('login'))
    

@app.route('/shop', methods=["GET","POST"])
def shop():
    return render_template('form.html')

@app.route('/add', methods=["GET","POST"])
def add():
     if request.method == "POST":

        product = request.form["product"]
        units = request.form["units"]
        color = request.form["color"] 

        #curl

        curl = mysql.connection.cursor()
        curl.execute("INSERT INTO products (product, units, color) VALUES (%s, %s, %s)",
        (product, units, color))

        #commit
        mysql.connection.commit()

        data = curl.fetchall()

        print(data)

        curl.close()

        #mensaje entre vistas
        flash("product added succesfully", "success")

        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)