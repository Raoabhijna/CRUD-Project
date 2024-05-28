import pymysql
from flask import request, render_template
from app import app
from database import mysql


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('home.html', title='HOME - Landing Page')

@app.route('/login', methods=['GET'])
def log():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global cursor
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql1 = cursor.execute(
            'SELECT * FROM admin WHERE username = % s \
            AND password = % s', (username, password, ))
        sql1 = cursor.fetchone()
        if sql1:
            return render_template('view.html', sql1=sql1)
        else:
            return None
            error = "invalid Username or Passowrd"
            return render_template('Login.html', error=error)
           # print(sql1)
    return render_template('Login.html')
    cursor.close()
    conn.close()

@app.route('/view', methods=['GET'])
def view():
    return render_template('view.html')

@app.route('/', methods=['GET'])
def add_student():
    return render_template('view.html', datas=fetchListOfstudents())


@app.route("/add", methods=["POST"])
def home():
    global cursor
    try:
        usn = request.form.get('usn')
        name = request.form.get('name')
        email = request.form.get('email')
        sem = request.form.get('sem')
        branch = request.form.get('branch')
        sql = "INSERT INTO student(usn, name, email,sem,branch) VALUES(%s, %s, %s ,  %s , %s)"
        data = (usn, name, email, sem, branch)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return render_template('view.html', datas=fetchListOfstudents())
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteStudent', methods=['POST'])
def deleteStudent():
    try:
        _usn = request.form.get('usn')
        print(_usn)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE usn=%s", (_usn))
        conn.commit()
        return render_template('view.html', datas=fetchListOfstudents())
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def fetchListOfstudents():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/StudentUpdate', methods=['POST'])
def update_student():
    try:
        usn = request.form.get('usn')
        name = request.form.get('name')
        email = request.form.get('email')
        sem = request.form.get('sem')
        branch = request.form.get('branch')
        sql = "UPDATE student SET name=%s, email=%s, sem=%s, branch=%s WHERE usn=%s"
        data = (name, email, sem, branch, usn,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return render_template('view.html', datas=fetchListOfstudents())
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
