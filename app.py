from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'mysql'

mysql = MySQL()
mysql.init_app(app)

@app.route("/add", methods=["POST"])  # Use POST method for adding data
def add_student():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Create a connection to the SQL instance
        conn = mysql.connection
        cursor = conn.cursor()

        # Use a parameterized query to prevent SQL injection
        sql = "INSERT INTO students (studentName, email) VALUES (%s, %s)"
        cursor.execute(sql, (name, email))
        conn.commit()

        return jsonify({"Result": "Success"})
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return jsonify({"Result": "Error", "Message": str(e)})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/students")  # Default - Show Data
def read():
    try:
        # Create a connection to the SQL instance
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM students')  # Execute an SQL statement
        results = cursor.fetchall()

        student_list = []
        for row in results:
            student = {
                "Name": row[0].replace('\n', ' '),
                "Email": row[1],
                "ID": row[2]
            }
            student_list.append(student)

        response = {
            'Results': student_list,
            'count': len(student_list)
        }

        return jsonify(response)
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return jsonify({"Result": "Error", "Message": str(e)})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)  # Run the Flask app on port 8080
