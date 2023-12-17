#from flask import Flask, request, jsonify
from flask import Flask, render_template, request, jsonify, send_from_directory
#from flask_swagger_ui import get_swaggerui_blueprint
import subprocess
import shlex
import os
import json
import requests

#load_dotenv()  # Load environment variables from .env file

#SWAGGER_URL = '/apidocs'  # URL for exposing Swagger UI (without trailing '/')
#API_URL = '/apispec.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
""" swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Command Execution API"
    },
) """

def create_app():
    app = Flask(__name__)
    #app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # API key for security
    API_KEY = os.environ.get('API_KEY', 'default_key')  # Set your API key in the environment

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

    @app.route('/execute', methods=['POST'])
    def execute_command():

        # Checking the API key
        print(request)
        print(request.remote_addr)
        api_key = request.headers.get('Authorization')
        print(api_key)
        print(API_KEY)
        
        if api_key is None:
            return jsonify({'error': 'No Authorization header provided'}), 400
        
        if api_key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.json
        if data is None:
            return jsonify({'error': 'No data provided'}), 400

        command = data.get('command')
        if command is None:
            return jsonify({'error': 'No command provided'}), 400

        server_address = data.get('serverAddress', None)
        server_api_key = data.get('serverAPIkey', None)
        if server_address and server_api_key:
            try:
                # Forward the request to the specified server address
                response = requests.post(f'{server_address}/execute', json={'command': command}, headers={'Authorization': server_api_key})
                response.raise_for_status()
                return jsonify(response.json()), response.status_code
            except requests.exceptions.RequestException as e:
                return jsonify({'error': str(e)}), 500


        # Basic security measures - if bridge???
        #allowed_commands = ['ls', 'echo', 'cat']
        #if not any(cmd in command for cmd in allowed_commands):
        #    return jsonify({'error': 'Command not allowed'}), 403

        # Avoid potentially dangerous commands
        if any(cmd in command for cmd in ['rm', 'mv', 'cp']):
            return jsonify({'error': 'Potentially dangerous command'}), 403

        try:
            # Check the operating system
            if os.name == 'nt':
                # On Windows, call PowerShell and pass the command as an argument
                process = subprocess.Popen(["powershell", "-Command"] + shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                # On Linux, just split the command
                process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = process.communicate()

            # Check if stderr is not empty
            if stderr:
                return stderr.decode()
                #return jsonify({'stdout': stdout.decode(), 'stderr': stderr.decode()})
            else:
                return stdout.decode()
                #return jsonify({'stdout': stdout.decode()})
        except Exception as e:
            return str(e)
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