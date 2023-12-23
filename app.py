from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import shlex
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Function to get the command interpreter based on the operating system
def get_command_interpreter():
    if os.name == 'nt':  # Windows
        try:
            # Check if PowerShell is available
            version = subprocess.check_output(["powershell", "$PSVersionTable.PSVersion.Major"], universal_newlines=True).strip()
            return "powershell", version
        except Exception:
            version = subprocess.check_output(["cmd", "/c", "ver"], universal_newlines=True).strip()
            return "cmd", version  # Default to cmd if PowerShell is not available
    else:  # Unix/Linux/Mac
        try:
            # Check if bash is available
            version = subprocess.check_output(["/bin/bash", "-c", "echo $BASH_VERSION"], universal_newlines=True).strip()
            return "/bin/bash", version
        except Exception:
            version = subprocess.check_output(["/bin/sh", "-c", "echo $SH_VERSION"], universal_newlines=True).strip()
            return "/bin/sh", version  # Default to sh if bash is not available

# Function to check if Python is available and get its version
def check_python():
    try:
        version = subprocess.check_output(["python", "--version"], universal_newlines=True).strip()
        return "python", version
    except Exception:
        return None, None

# Function to create the Flask app
def create_app():
    app = Flask(__name__)
    print("♣️ ClubGPT ♣️ - CommandProxy")

    # CP_MODE options (see .env.example)
    CP_MODE = os.environ.get('CP_MODE', 'BRIDGE')  # Set your CP_MODE in the environment
    print(f"CP_MODE: {CP_MODE}")

    # KEY_MODE options (see .env.example)
    KEY_MODE = os.environ.get('KEY_MODE', 'SESSION_KEY')  # Set your KEY_MODE in the environment
    print(f"KEY_MODE: {KEY_MODE}")
   
    # API key for security
    # If KEY_MODE is SESSION_KEY or no API_KEY is available, generate a random 16-character string using secrets
    if KEY_MODE == 'SESSION_KEY' or not os.environ.get('API_KEY'):
        import secrets
        API_KEY = secrets.token_hex(16)
        print(f"API_KEY: {API_KEY}")
    else:
        API_KEY = os.environ.get('API_KEY')
        print(f"API_KEY: {API_KEY}")

    @app.route('/apispec.json')
    def spec():
        with open('apispec.json', 'r') as f:
            json_content = json.load(f)
        return jsonify(json_content)

    #@app.route('/.well-known/acme-challenge/<path:filename>')
    #def acme_challenge(filename):
    #    return send_from_directory(os.path.join(app.root_path, '.well-known', 'acme-challenge'), filename)

    @app.route('/docs')
    def docs():
        return render_template('docs.html')

    @app.route('/info')
    def info():
        return "For more info visit https://clubgpt.info"

    @app.route('/system_info', methods=['POST'])
    def system_info():

        data = request.json
        if data is None:
            return jsonify({'error': 'No data provided'}), 400

        server_address = data.get('serverAddress', None)
        server_api_key = data.get('serverAPIkey', None)
        if server_address and server_api_key:
            try:
                # Forward the request to the specified server address
                response = requests.post(f"{server_address}/system_info", json={}, headers={"Authorization": server_api_key}, verify=False)
                response.raise_for_status()

                #stdout = response.content
                #return stdout
                return jsonify(response.json()['content'])
                return jsonify(response.json()), response.status_code
            
            except requests.exceptions.RequestException as e:
                return jsonify({'error': str(e)}), 500
        
        interpreter, interpreter_version = get_command_interpreter()
        python, python_version = check_python()

        if python:
            python_info = f"Python version: {python_version}"
        else:
            python_info = "Python is not available"

        CP_MODE = os.environ.get('CP_MODE', 'BRIDGE')
        KEY_MODE = os.environ.get('KEY_MODE', 'SESSION_KEY')

        return jsonify({
            "Interpreter": interpreter,
            "Interpreter Version": interpreter_version,
            "Python Info": python_info,
            "CP_MODE": CP_MODE,
            "KEY_MODE": KEY_MODE
        })

    # Route to execute a command
    @app.route('/execute', methods=['POST'])
    def execute_command():

        # Checking the API key
        print(request)
        api_key = request.headers.get('Authorization')
        print(api_key)
        print(API_KEY)
        
        if api_key is None:
            return jsonify({'error': 'No Authorization header provided'}), 400
        
        if api_key != API_KEY:
            return jsonify({'error': 'Unauthorized, API key is not matching', 'provided_key': api_key, 'expected_key': API_KEY}), 401
        
        data = request.json
        if data is None:
            return jsonify({'error': 'No data provided in request'}), 400

        command = data.get('command')
        if command is None:
            return jsonify({'error': 'No command provided'}), 400

        server_address = data.get('serverAddress', None)
        server_api_key = data.get('serverAPIkey', None)
        if server_address and server_api_key:
            try:
                # Forward the request to the specified server address
                response = requests.post(f'{server_address}/execute', json={'command': command}, headers={'Authorization': server_api_key}, verify=False)
                response.raise_for_status()

                stdout = response.content
                return stdout
                return jsonify(response.json()['content'])
                return jsonify(response.json()), response.status_code
            
            except requests.exceptions.RequestException as e:
                return jsonify({'error': str(e)}), 500

        # Basic security measures in BRIDGE mode
        if os.environ.get('CP_MODE') != 'SERVER':
            allowed_commands = ['curl', 'echo', 'ping']
            if not any(cmd in command for cmd in allowed_commands):
                return jsonify({'error': '♣️ Command not allowed in BRIDGE mode'}), 403

        # Avoid potentially dangerous commands
        #if any(cmd in command for cmd in ['rm', 'mv', 'cp']):
        #    return jsonify({'error': 'Potentially dangerous command'}), 403

        try:
            # Check the operating system
            interpreter, _ = data.get('interpreter', get_command_interpreter())
            if interpreter == 'powershell':
                # On Windows, call PowerShell and pass the command as an argument
                process = subprocess.Popen(["powershell", "-Command"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif interpreter == 'cmd':
                # On Windows, call cmd and pass the command as an argument
                process = subprocess.Popen(["cmd", "/c"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif interpreter == '/bin/bash':
                # On Linux, call bash and pass the command as an argument
                process = subprocess.Popen(["/bin/bash", "-c"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif interpreter == '/bin/sh':
                # On Linux, call sh and pass the command as an argument
                process = subprocess.Popen(["/bin/sh", "-c"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif interpreter == 'python':
                # Call Python and pass the command as an argument
                process = subprocess.Popen(["python", "-c"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                # Default to shlex.split(command)
                process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()

            # Check if stderr is not empty
            if stderr:
                #return stderr.decode()
                return jsonify({'stdout': stdout.decode(), 'stderr': stderr.decode()})
            else:
                #return stdout.decode()
                return jsonify({'stdout': stdout.decode()})
        except Exception as e:
            #return str(e)
            return jsonify({'error': str(e)})

    return app

app = create_app()

# Run the app if this file is executed directly
if __name__ == '__main__':
    if os.path.isfile('certificates/cert.pem') and os.path.isfile('certificates/key.pem'):
        import socket
        host = socket.gethostbyname(socket.gethostname())
        app.run(debug=False, host=host, port=5000, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
    else:
        app.run(debug=False)