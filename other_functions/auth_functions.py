from flask import render_template, request, redirect, session
from other_functions.db import get_db

def sign_up():
    error =""
    if request.method == "POST":
        
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']

        try:
            if password != re_password:
                error = "Password Don't match"

            else:
                db = get_db()
                c = db.cursor()

                c.execute("insert into users (Name, Email, username, password) values (?, ?, ?, ?)",(name, email, username, password))
                db.commit()
                db.close()

                session['user_id'] = c.lastrowid         
                session["username"] = username

                return redirect('/home')
            
        except Exception as e:
            error = str(e)

    return render_template("sign_up.html", error = error)

# -------------------------------------------------------------

def login():
    error =""
    if request.method == "POST":
        
        username = request.form['username']
        password = request.form['password']

        try:
            db = get_db()
            c = db.cursor()
            
            c.execute("select id,username,password,is_admin from users where username =? and password = ? ",(username,password))
            user = c.fetchone()

            if user :
                session['user_id'] = user[0]    #for uniqe
                session['username'] = user[1]  
                session["is_admin"] = user[3]           

                return redirect('/home')
            
            else : error = "User Not Found or Password Incorrect"

        except Exception as e:
            error = str(e)

    return render_template("login.html", error = error)