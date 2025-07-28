from flask import render_template, request, redirect, session
from other_functions.db import get_db


def add_student():
    user = session.get('username')
    error =''
    msg =''
    if user:
        try:
            if request.method == "POST":
                id = request.form["id"]
                name = request.form["name"]
                age = request.form["age"]
                course = request.form["course"]
                year = request.form["year"]

                with get_db() as db:
                    c = db.cursor()

                    c.execute("insert into students(id ,name, age,course, year,username,user_id) values(?,?,?,?,?,?,?)",(id,name,age,course,year,user,session.get('user_id')))
                    
                    db.commit()
                    msg = "Student Added successfully"

        except Exception as e:
            error = str(e) + " (Student ID must be unique)"

    else:
        return redirect('/')
    
    return render_template("add_student.html" ,error = error,msg = msg)

def delete_student():
    user = session.get('username')
    error =''
    msg =''
    if user:
        if request.method == "POST":
            id = request.form["id"]

            try:
                with get_db() as db:

                    ans = db.execute("DELETE FROM students WHERE id = ? AND user_id = ?", (id, session.get('user_id')))
                    db.commit()

                    if ans.rowcount != 0:
                        msg = f"Student with ID {id} deleted successfully"

                    else:
                        error = f"No student found with ID {id}"

            except Exception as e:
                error = "Error deleting student:"+str(e)

    else:
        return redirect('/')
    
    return render_template("delete_student.html" ,error = error,msg = msg)

def search_student():
    user = session.get('username')
    error = ''
    msg = ''
    students = []

    if user:
        if request.method == "POST":
            try:
                with get_db() as db:

                    if request.form.get("show_all"):
                        students = db.execute("SELECT * FROM students WHERE user_id = ?", (session.get('user_id'),)).fetchall()
                        msg = f"{len(students)} student(s) found"

                    else:
                        ch = request.form["field"]
                        value = request.form["value"]
                
                        query = f"SELECT * FROM students WHERE {ch} = ? AND user_id = ?"
                        students = db.execute(query, (value, session.get('user_id'))).fetchall()

                        if students:
                            msg = f"{len(students)} student(s) found"
                        else:
                            error = "No student found"

            except Exception as e:
                error = str(e)
    else:
        return redirect('/')

    return render_template("search_student.html", error=error, msg=msg, students=students)

def update_student():
    user = session.get('username')
    error = ''
    msg = ''

    if not user:
        return redirect('/')

    if request.method == "POST":
        student_id = request.form["id"]
        name = request.form.get("name")
        age = request.form.get("age")
        course = request.form.get("course")

        if not any([name, age, course]):
            error = "Please provide at least one field to update."
        else:
            try:
                with get_db() as db:
                    result = db.execute("SELECT * FROM students WHERE id = ? AND user_id = ?", (student_id, session.get('user_id'))).fetchone()
                    if not result:
                        error = "Student not found."
                    else:
                        if name:
                            db.execute("UPDATE students SET name = ? WHERE id = ? AND user_id = ?", (name, student_id, session.get('user_id')))
                        if age:
                            db.execute("UPDATE students SET age = ? WHERE id = ? AND user_id = ?", (age, student_id, session.get('user_id')))
                        if course:
                            db.execute("UPDATE students SET course = ? WHERE id = ? AND user_id = ?", (course, student_id, session.get('user_id')))
                        db.commit()
                        msg = "Student record updated successfully."

            except Exception as e:
                error = "Error updating student: " + str(e)

    return render_template("update_student.html", error=error, msg=msg)
