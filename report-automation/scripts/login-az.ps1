# Login to Azure Powershell
$password = ConvertTo-SecureString -String $env:az_user_pwd -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($env:az_user, $password)
Connect-AzAccount -TenantId $env:az_tenant_id -Credential $cred
# Get user acess token
$token = (Get-AzAccessToken -ResourceUrl 'https://management.azure.com').Token
# Remove API_KEY from .env file
$dotenvfilepath = "../../.env"
$content = Get-Content $dotenvfilepath | Select-String -Pattern "API_KEY" -NotMatch
Set-Content -Path $dotenvfilepath -Value $content
# Update .env file with new user acess token
$api_key = "API_KEY=$token"
Write-Output $api_key >> $dotenvfilepath