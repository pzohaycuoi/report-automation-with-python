try {
  $password = ConvertTo-SecureString -String $env:az_user_pwd -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential($env:az_user, $password)
  Connect-AzAccount -ServicePrincipal -TenantId $env:az_tenant_id -Credential $cred
  $token = (Get-AzAccessToken -ResourceUrl 'https://management.azure.com').Token
  Write-Output $token
}
catch {
  # TODO: handling error
}