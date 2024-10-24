import subprocess
import os
from time import sleep
from datetime import datetime, timedelta

# Function to check if a package is installed, and install it if not
def check_package(package_name):
    try:
        __import__(package_name)
        print(f"{package_name} is already installed.")
    except ImportError:
        print(f"{package_name} is not installed. Installing now...")
        subprocess.check_call(["python", "-m", "pip", "install", package_name])

# Check necessary packages
check_package("flask")
from flask import Flask, render_template, jsonify

app = Flask(__name__)

exam_info = {
    'exam_venue': 'E-90837',
    'subject_code': 'MuEM2-1',
    'start_time': '2024-11-14 05:30:00',
    'end_time': '2024-11-14 10:15:00',
    'current_time': '',
    'remaining_time': ''
}

# Define route for the home page
@app.route('/')
def home():
    return render_template('index.html', exam_info=exam_info)

@app.route('/time-info')
def time_info():
    global exam_info
    start_time = datetime.strptime(exam_info['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(exam_info['end_time'], "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow() + timedelta(hours=8)  # Current time adjusted by 8 hours

    if now < start_time:
        remaining_time = end_time - start_time
    elif now < end_time:
        remaining_time = end_time - now
    else:
        remaining_time = timedelta(seconds=0)

    # Format remaining time as HH:mm:ss
    total_seconds = int(remaining_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")  # Format current time

    # Create response data
    response = jsonify({
        'current_time': current_time_str,
        'remaining_time': remaining_time_str
    })
    response.headers.add('Cache-Control', 'no-store')  # No caching
    return response

# Run the Flask app
if __name__ == '__main__':    
    os.system("start http://localhost:316")  # Open the app in the default web browser
    app.run(port=316, debug=False)