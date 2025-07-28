from flask import render_template, request, redirect, session
from other_functions.db import get_db

def users():

    if session.get('username') and session.get('is_admin') == 1:

        with get_db() as db:
            c = db.cursor()
            user_data = c.execute("select * from users order by id").fetchall()
            total_users = len(user_data)

    else :
        return redirect('/')

    return render_template("Admin_page/users_view.html", users = user_data,total_users = total_users)


def students():
    if session.get('username') and session.get('is_admin') == 1:

        with get_db() as db:
            c = db.cursor()
            students_data = c.execute("select * from students order by id").fetchall()
            total_students = len(students_data)

    else :
        return redirect('/')

    return render_template("Admin_page/students_view.html", students = students_data,total_students = total_students)


def delete_user(user_id):
    error =''
    msg =''

    if not session.get('username') or session.get('is_admin') != 1:
        return redirect('/')

    # if admin trying to delete admin data 
    if int(user_id) == int(session.get("user_id")): 
        error = "You cannot delete your own admin account."
    else:
        with get_db() as db:
            db.execute("delete from users where id = ?", (user_id,))
            db.commit()
            msg = 'user deleted successfully'

    with get_db() as db:
        c = db.cursor()
        user_data = c.execute("SELECT * FROM users ORDER BY id").fetchall()
        total_users = len(user_data)

    return render_template("Admin_page/users_view.html",error = error,msg = msg,users=user_data,total_users = total_users)