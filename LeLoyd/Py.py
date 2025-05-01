from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to the database
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crud_db"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = db_connection()
    cursor = conn.cursor()

    # Get filter values from the form
    min_score = request.args.get('min_score', default=None, type=int)
    max_score = request.args.get('max_score', default=None, type=int)

    # If both min_score and max_score are provided, apply the filter
    if min_score is not None and max_score is not None:
        cursor.execute("SELECT * FROM students WHERE score BETWEEN %s AND %s", (min_score, max_score))
    elif min_score is not None:  # If only min_score is provided
        cursor.execute("SELECT * FROM students WHERE score >= %s", (min_score,))
    elif max_score is not None:  # If only max_score is provided
        cursor.execute("SELECT * FROM students WHERE score <= %s", (max_score,))
    else:  # Default: show all students
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    conn.close()

    return render_template("index.html", students=students)



@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    score = request.form['score']
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, score) VALUES (%s, %s, %s)", (name, email, score))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        score = request.form['score']
        cursor.execute("UPDATE students SET name=%s, email=%s, score=%s WHERE id=%s", (name, email, score, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template("edit.html", student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
