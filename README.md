****** WORK IN PROGRESS ******

# ClubGPT - CommandProxy
OpenAPI 3.1 compatible service which enables ChatGPT GPTs to run shell commands as an action on any computer (powershell, bash).

Use at you own risk. Be careful, this is basically opening up a 

## Introduction

Using this tool and having ChatGPT Plus you can run any shell commands on your computer as an action.

There are of course other approaches using local language models or LLM APIs, running them locally (like [Open Interpreter](https://github.com/KillianLucas/open-interpreter) or [PowerShellAI](https://github.com/dfinke/PowerShellAI)) or on a remote sandbox (like [ClubGPT-Sandbox](https://github.com/matebenyovszky/ClubGPT-Sandbox)), which are all also cool, but I wanted to try how far can I go with this approach.

This is a Flask API that allows executing commands on the server. It uses an API key for authorization.

## Setup

1. Install the required Python packages:
pip install -r requirements.txt

2. Configuration
CP_MODE options:
* SERVER: a worker (executor) that can run commands, could also act as a bridge
* BRIDGE: cannot execute commands in the environment, just forward them. This is the default.

KEY_MODE options
* DEFAULT: Default key. This is the default.
* ENV_KEY: API key defined in the .env file.
* SESSION_KEY: Random key every time you. This is the default.

3. Run the application:
python app.py

## Usage

You can execute a command on the server by making a POST request to the `/execute` endpoint. Here's a sample `curl` command:

bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: your_api_key" -d '{"command":"ls"}' %URL%/execute


curl -X POST "%URL%/execute" -H "Authorization: your_secret_api_key_here" -H "Content-Type: application/json" -d '{"command":"ls"}'

Replace `your_api_key` with your actual API key.

## Security

This API uses an API key for authorization. The API key is set in the environment variable `API_KEY`. If `API_KEY` is not set, the default key is `default_key`.

The API also has some basic security measures to prevent potentially dangerous commands from being executed. For example, it does not allow commands that include `rm`, `mv`, or `cp`.

Notes:


### Local / remote server / worker app

To use the PDF crawler, follow these steps:

1. Install the required packages from `requirements.txt`.
2. Collect underpants.
3. Define the necessary environment variables.
4. Run the `app.py` file to start.

### Local / remote server / worker publishing

On my home router:
I use port forwarding rule to publish port 5000.

Optional:
* Dynamic DNS
* Let's Encrypt
* Download key.pem and cert.pem into "certificates" directory

### Bridge mode

Bridge mode was required because I cannot make it work directly with ChatGPT, so I made az Azure Web App to forward commands.

### Contributions

Contributions are welcome! Submit a pull request with any improvements or bug fixes.

### License

This project is licensed under Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.md](LICENSE.md) file for details.