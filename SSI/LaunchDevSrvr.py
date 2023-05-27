import os
import subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.Popen(["python", "-m", "webbrowser", "-t", "http://localhost:8000/"])
subprocess.run(["python", "manage.py", "runserver"])