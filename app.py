from flask import Flask, render_template, jsonify
import subprocess
import program1


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('next.html')

@app.route('/capture_attendance', methods=['POST'])
def capture_attendance():
    try:
        # Run the program.py script using subprocess
        subprocess.run(['python', 'program1.py'], check=True)
        result = {"result": "Attendance capture completed."}
    except subprocess.CalledProcessError as e:
        result = {"result": f"Error: {e}"}

    return jsonify(result)

@app.route('/redirect_example')
def redirect_example():
    return render_template('next.html')

if __name__ == '__main__':
    app.run(debug=True)
