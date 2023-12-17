$response = 0

# API URL
$url = 'https://command-proxy.azurewebsites.net/execute'
$url = 'https://d168.asuscomm.com/execute'

# API Key
$headers = @{"Authorization" = "your_secret_api_key_here"}

# Data Payload
$body = @{
    "command" = "echo Hello World!"
} | ConvertTo-Json

# Send POST Request
$response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"

# Display the Response
$response
#$response.stdout # If JSON