$response = 0

# API URL
$url = 'https://commandproxy.azurewebsites.net/execute'
$url = 'https://d168.asuscomm.com/execute'

# API Key
$headers = @{"Authorization" = "your_secret_api_key_here"}
#$headers = @{"Authorization" = "default_key"}

# Data Payload
$body = @{
    "command" = "echo Hello World!"
    "serverAddress" = "https://commandproxy.azurewebsites.net"
    "serverAPIkey" = "default_key"
} | ConvertTo-Json


# Send POST Request
$response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"

# Display the Response
$response
#$response.stdout # If JSON