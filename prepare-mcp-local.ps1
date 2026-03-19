[CmdletBinding()]
param(
    [switch]$InstallDependencies = $true,
    [switch]$RunValidation = $true
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

Set-Location $PSScriptRoot

Write-Step "Checking local osTicket lab"
$dockerExe = (Get-Command docker -ErrorAction Stop).Source

& $dockerExe compose ps --status running *> $null
if ($LASTEXITCODE -ne 0) {
    throw "The local stack is not running. Run install-local.cmd first."
}

Write-Step "Checking osTicket database schema"
$schemaCheck = & $dockerExe compose exec -T mysql mysql -h 127.0.0.1 -u root -prootpassword osticket -N -e "SHOW TABLES LIKE 'ost_form';"
if ($LASTEXITCODE -ne 0 -or -not ($schemaCheck | Select-String -SimpleMatch 'ost_form')) {
    throw "The osTicket schema is not installed yet. Run install-local.cmd or install-local.ps1 -ResetData first."
}

Write-Step "Normalizing running osTicket config"
& $dockerExe compose exec -T `
    -e "OST_LOCAL_SECRET_SALT=H0leyTT06xifGvsdDpYD7VupNviICd3r" `
    -e "OST_LOCAL_ADMIN_EMAIL=admin@local.test" `
    -e "OST_LOCAL_DBHOST=mysql" `
    -e "OST_LOCAL_DBNAME=osticket" `
    -e "OST_LOCAL_DBUSER=osticket" `
    -e "OST_LOCAL_DBPASS=osticket123" `
    -e "OST_LOCAL_DBPREFIX=ost_" `
    osticket php /usr/src/osticket/configure_local_install.php
if ($LASTEXITCODE -ne 0) {
    throw "Failed to normalize the running osTicket config."
}

if ($InstallDependencies) {
    Write-Step "Installing MCP Python dependencies"
    python -m pip install -r "$PSScriptRoot\mcp-server\requirements.txt"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install MCP Python dependencies."
    }
}

if ($RunValidation) {
    Write-Step "Validating osTicket MCP locally"
    $env:OSTICKET_URL = 'http://localhost:8080'
    $env:OSTICKET_BACKEND = 'local'
    $env:OSTICKET_DOCKER_PROJECT_DIR = $PSScriptRoot
    $env:DOCKER_EXE = $dockerExe

    Push-Location "$PSScriptRoot\mcp-server"
    try {
        python test.py
        if ($LASTEXITCODE -ne 0) {
            throw "MCP validation failed."
        }
    }
    finally {
        Pop-Location
    }
}

Write-Step "MCP lab is ready"
Write-Host "Local app : http://localhost:8080/"
Write-Host "Admin     : http://localhost:8080/scp/"
Write-Host "MCP       : ${PSScriptRoot}\mcp-server\server.py"