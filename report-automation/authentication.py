from dotenv import load_dotenv
import os
import subprocess


load_dotenv()
script_path = './report-automation-with-python/report-automation/scripts/login-az.ps1'
output = subprocess.run(f'pwsh {script_path} -UserName {os.getenv("AZURE_USERNAME")} -Password {os.getenv("AZURE_PASSWORD")} -TenantID {os.getenv("AZURE_TENANT_ID")}', capture_output=False)
