# ClubGPT - CommandProxy
```
          =*##*=
        -@@@@@@@@-
        @@@@@@@@@@
        %@@@@@@@@%            .g8"""bgd `7MM            *MM          .g8"bgd `7MM""Mq. MMP"MM"YMM
   .---:.#@@@@@@%.:---.     .dP'     `M   MM             MM        .dP'   `M   MM  `MM.P'  MM  `7
 -%@@@@@@*#@@@@#*@@@@@@%=   dM'       `   MM `7MM  `7MM  MM,dMMb.  dM'     `   MM  ,M9     MM
-@@@@@@@@@@@@@@@@@@@@@@@@=  MM            MM   MM    MM  MM    `Mb MM          MMmdM9      MM
=@@@@@@@@@@@@@@@@@@@@@@@@+  MM.           MM   MM    MM  MM     M8 MM.  `7MMF' MM          MM
 *@@@@@@@@++@@*+@@@@@@@@*   `Mb.     ,'   MM   MM    MM  MM.   ,M9 `Mb.   MM   MM          MM
  .=***=: .@@@@. :=***=.      `"bmmmd'  .JMML. `Mbod"YML.P^YbmdP'    `"bmdPY .JMML.      .JMML.
          #@@@@%
         *@@@@@@#
        =#**++***=
```
This repository provides an OpenAPI 3.1 compatible service that allows ChatGPT and other GPT models to execute commands on any computer, supporting various shells such as PowerShell, Bash, etc. Essentially, it enables remote task execution on your computer using natural language prompts.

Please note that this tool should be used with caution and at your own risk.

# Members of the ClubGPT agent tool/family
## Agent group prompts
- [♣️ ClubGPT - DevTeam](https://github.com/matebenyovszky/ClubGPT) - It's a think tank, coding companion, a developer team in one GPT
- [♣️ ClubGPT - DreamTeam](https://github.com/matebenyovszky/ClubGPT) - a more general approach, where the AI selects team members and tools according to the task

## Workshop and Tools for the Agents
- ♣️ ClubGPT - CommandProxy - (this repository) Enables the execution of commands and code on a remote computer.
- ♣️ ClubGPT - Sandbox - Provides a secure environment for code execution.
- [♣️ ClubGPT - Sandbox-ts](https://github.com/matebenyovszky/ClubGPT-Sandbox-ts) - A TypeScript version of the sandbox for code execution.

# Overview

This tool, in conjunction with ChatGPT Plus, allows you to execute any shell commands on a computer as an action.

While there are other methods that utilize local language models or LLM APIs, running them locally (such as [Open Interpreter](https://github.com/KillianLucas/open-interpreter) or [PowerShellAI](https://github.com/dfinke/PowerShellAI)) or in a remote sandbox (like [ClubGPT-Sandbox](https://github.com/matebenyovszky/ClubGPT-Sandbox)), this tool offers a unique approach to remote command execution.

## Features and Highlights

- Provides a Flask API for executing commands on a machine (PowerShell/CMD/Shell/Bash/Python etc.).
- Utilizes an API key for authorization, which can be either fixed or generated for each session, ensuring your machine is not exposed to ChatGPT long-term.
- Includes a separate endpoint to retrieve basic system information (/system_info).
- Offers a Bridge mode to forward requests to another worker. This mode was developed to facilitate direct interaction with ChatGPT, using an Azure Web App to forward commands.

## Samples and ideas

[View some sample screenshots of usage in ChatGPT here](images/)

## Setup

1. Install the required Python packages:
```pip install -r requirements.txt```

2. Configuration

- CP_MODE options:
  - SERVER: A worker (executor) that can run commands, could also act as a bridge.
  - BRIDGE: Cannot execute commands in the environment, just forward them. This is the default.

- KEY_MODE options:
  - ENV_KEY: API key defined in the .env file.
  - SESSION_KEY: Random key generated every time you start a session. This is the default.

- VERBOSE options:
  - ON: Detailed logs will be made locally. This is the default.
  - OFF: No detailed logs will be made.

3. Run the application:
python app.py

4. Maker you machine accessible from the internet, accessible by ChatGPT.

In my case I've set up a Dynamic DNS with Let's Encrypt certificates and port forwarding in my computer (published my computer's port 5000 on 443). Downloaded key.pem and cert.pem from the router into "certificates" directory so I could start my Flask application with those.

5. Create a GPT

You can use this [prompt](prompts.example.md) as an instruction, where if you optionally set the base data you can start quicker.

6. Add GPT action

Create new action, import URL from your server `https://%URL%/apispec.json`.
Set Authentication to "API Key" with header name "Authorization".

![Setup Action](images/setup_action_authentication.jpg)

7. Have fun

## Usage from API calls

You can execute a command on the server by making a POST request to the `/execute` endpoint. Here's a sample `curl` command:

```bash
curl -X POST "%URL%/execute" -H "Authorization: your_secret_api_key_here" -H "Content-Type: application/json" -d '{"command":"ls"}'
```

Samples in `powershell`:
1. Get system info:

```powershell
$url = '%URL%/system_info' # API URL
$headers = @{"Authorization" = "your_secret_api_key_here"} # API Key

$body = @{
    #"serverAddress" = "optional_remote_%URL%"
    #"serverAPIkey" = "optional_remote_your_secret_api_key_here"
} | ConvertTo-Json

# Send Post Request
$response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"

# Display the Response
$response
```

2. Execute a command:

```powershell
$url = '%URL%/execute' # API URL
$headers = @{"Authorization" = "your_secret_api_key_here"} # API Key

$body = @{
    "command" = "echo Hello World!"
    #"serverAddress" = "optional_remote_%URL%"
    #"serverAPIkey" = "optional_remote_your_secret_api_key_here"
} | ConvertTo-Json

# Send POST Request
$response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"

# Display the Response
$response.stdout
```

Replace `%URL%` and `your_secret_api_key_here` with your actual API key.

## Security

This API uses an API key for authorization. The API key is set in the environment variable `API_KEY`. If `API_KEY` is not set, the application will generate one.

But be aware, that this is only a POC, can be considered as a backdoor to your machine, not intended for production etc... so use at your own risk.

### Contributions

Contributions are welcome! Submit a pull request with any improvements or bug fixes.

### License

This project is licensed under Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.md](LICENSE.md) file for details.