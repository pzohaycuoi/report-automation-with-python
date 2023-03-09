# TODO: this script will run in Nifi server before anything else

## Setting up the environment and install prerequiste package ##
$PowershellVersion = $PSVersionTable.PSVersion
Write-Host "Current Powershell version is: $($PowershellVersion.Major).$($PowershellVersion.Minor)"
if ($PowershellVersion.Major -lt 7) {
  Write-Host "Powershell version is lower then 7, updating..."
  winget install --id Microsoft.Powershell --source winget
}

if ((Get-Module -ListAvailable -Name Az.Accounts) -eq $null) {
  Write-Host "Powershell Az.Accounts module is not installed, installing..."
  Install-Module Az.Accounts -Force -Verbose
} else {
  Write-Host "Powershell Az.Accounts module already installed"
}

## Install python and required dependencies ##
$PythonVersion = Get-Command python
if ($PythonVersion -eq $null) {
  Write-Host "Python is not installed, installing..."
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
  choco install -y python3
} else {
  Write-Host "Python is already installed"
}

if ($PythonVersion.Version.Major -ne 3) {
  Write-Host "Python version is lower than 3, installing python 3..."
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
  choco install -y python3
}

if ($PythonVersion.Version.Minor -lt 11) {
  Write-Host "Python version is lower than 3.11, Updating python..."
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
  choco install -y python3
}

Write-Host "Python version is: $($PythonVersion.Version)"
## Check environment existence ##