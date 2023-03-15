param (
  [Parameter(Mandatory)]
  [string]
  $UserName,

  [Parameter(Mandatory)]
  [string]
  $Password,

  [Parameter(Mandatory)]
  [string]
  $TenantID
)
begin {
  # Import module
  Import-Module Az.Accounts -Force
}
process {
  # Login to Azure Powershell
  $SecPass = ConvertTo-SecureString $Password -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential("$UserName", $SecPass)
  Connect-AzAccount -TenantId $TenantID -Credential $cred
  # Get user acess token
  $token = (Get-AzAccessToken -ResourceUrl 'https://management.azure.com').Token
  # Remove API_KEY from .env file
  $dotenvfilepath = "C:\Users\namng\report-automation-with-python\.env"
  # $dotenvfilepath = "../../.env"
  $content = Get-Content $dotenvfilepath | Select-String -Pattern "API_KEY" -NotMatch
  Set-Content -Path $dotenvfilepath -Value $content
  # Update .env file with new user acess token
  $api_key = "API_KEY=$token"
  Write-Output $api_key >> $dotenvfilepath
}

