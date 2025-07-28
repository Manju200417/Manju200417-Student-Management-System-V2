from flask import Flask,render_template,redirect,session
from other_functions.db import init_db
from other_functions.auth_functions import sign_up,login
from other_functions.Student_Route_finctions import add_student,delete_student,search_student,update_student
from other_functions.users_students_view import users,students,delete_user


app = Flask(__name__)
app.secret_key = "mmmmmmmm"

init_db()

try:
    # ---------------------LOGIN-SIGN_UP----------------------------------------

    @app.route('/sign_up',methods=["POST","GET"])
    def signup_route():
        return sign_up()

    @app.route('/',methods=["POST","GET"])
    def login_route():
        return login()

    # -------------------------------------------------------------

    @app.route('/home', methods=["POST", "GET"])
    def main_page():
        user = session.get('username')
        if user:
            if session.get("is_admin") ==1 :
               return redirect("/admin")
            
            else :
                return render_template('home.html',username = user)
            
        else :
            return redirect('/')

    # -------------------------------------------------------------


    @app.route('/add_student', methods=["POST", "GET"])
    def add_student_route():
        return add_student()

    @app.route('/delete_student', methods=["POST", "GET"])
    def delete_student_route():
        return delete_student()

    @app.route('/update_student', methods=["POST", "GET"])
    def update_student_route():
        return update_student()

    @app.route('/search_student', methods=["POST", "GET"])
    def search_student_route():
        return search_student()

    # -----------------------------admin--------------------------------


    @app.route('/admin', methods=["POST", "GET"])
    def admi_route():
        if session.get('username') and session.get('is_admin') == 1:
           return render_template("Admin_page/admin_dashboard.html")
        else:
            return redirect('/')


    @app.route('/admin/users_view')
    def users_route():
        return users()
    
    @app.route('/admin/delete_user/<int:user_id>')
    def delete_user_route(user_id):
        return delete_user(user_id)

    
    @app.route('/admin/students_view')
    def students_route():
        return students()

    # ---------------------------------------------------------------------

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    
except Exception as e:
    print("Error :",e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)