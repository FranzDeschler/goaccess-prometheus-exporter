import json
import os
import subprocess

def parse_log():
    script_path = os.path.dirname(__file__)
    goaccess = os.path.join(script_path, "run_goaccess.sh")

    subprocess.call([goaccess])

    output_file = os.path.join(script_path, "metrics.json")
    with open(output_file) as file:
        return json.loads(file.read())
