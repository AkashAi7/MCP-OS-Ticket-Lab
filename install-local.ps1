[CmdletBinding()]
param(
    [string]$HelpdeskName = "Local osTicket Demo",
    [string]$SystemEmail = "support@local.test",
    [string]$AdminFirstName = "Local",
    [string]$AdminLastName = "Admin",
    [string]$AdminEmail = "admin@local.test",
    [string]$AdminUsername = "ostadmin",
    [string]$AdminPassword = "ChangeMe123!",
    [string]$DbHost = "mysql",
    [string]$DbName = "osticket",
    [string]$DbUser = "osticket",
    [string]$DbPassword = "osticket123",
    [string]$TablePrefix = "ost_",
    [switch]$ImportSampleTickets = $true,
    [switch]$OpenBrowser = $true,
    [switch]$ResetData
)

$ErrorActionPreference = "Stop"
$script:DockerExe = $null

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Wait-Until {
    param(
        [scriptblock]$Condition,
        [string]$Description,
        [int]$TimeoutSeconds = 300,
        [int]$DelaySeconds = 5
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (& $Condition) {
            return
        }
        Start-Sleep -Seconds $DelaySeconds
    }

    throw "Timed out waiting for $Description."
}

function Ensure-DockerDaemon {
    Write-Step "Checking Docker"

    try {
        $script:DockerExe = (Get-Command docker -ErrorAction Stop).Source
    }
    catch {
        $candidatePaths = @(
            "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
            "C:\Program Files\Docker\Docker\resources\docker.exe"
        )
        $script:DockerExe = $candidatePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    }

    if (-not $script:DockerExe) {
        throw "docker.exe was not found. Install Docker Desktop first."
    }

    $daemonReady = $false
    try {
        & $script:DockerExe info *> $null
        $daemonReady = $true
    }
    catch {
        $dockerDesktop = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $dockerDesktop) {
            Write-Host "Starting Docker Desktop..."
            Start-Process $dockerDesktop | Out-Null
        }
    }

    if (-not $daemonReady) {
        Wait-Until -Description "Docker daemon" -TimeoutSeconds 240 -DelaySeconds 5 -Condition {
            try {
                & $script:DockerExe info *> $null
                return $true
            }
            catch {
                return $false
            }
        }
    }
}

function Invoke-Compose {
    param([string[]]$Arguments)
    & $script:DockerExe compose @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose $($Arguments -join ' ') failed."
    }
}

function Test-OsTicketInstalled {
    try {
        $schemaReady = Test-OsTicketSchemaReady
        if (-not $schemaReady) {
            return $false
        }

        $response = Invoke-WebRequest -Uri "http://localhost:8080/scp/" -UseBasicParsing -TimeoutSec 20
        if ($response.BaseResponse.ResponseUri.AbsoluteUri -like "*/setup/install.php*") {
            return $false
        }

        return $response.Content -match "Staff Control Panel|Authentication Required|Log In"
    }
    catch {
        return $false
    }
}

function Test-OsTicketSchemaReady {
    $result = & $script:DockerExe compose exec -T mysql mysql -h 127.0.0.1 -u root -prootpassword $DbName -N -e "SHOW TABLES LIKE '${TablePrefix}form';"
    if ($LASTEXITCODE -ne 0) {
        return $false
    }

    return ($result | Select-String -SimpleMatch "${TablePrefix}form") -ne $null
}

function Test-OsTicketConfigResolved {
    & $script:DockerExe compose exec -T osticket sh -lc "grep -q '%CONFIG-' /var/www/html/include/ost-config.php"
    if ($LASTEXITCODE -eq 0) {
        return $false
    }
    if ($LASTEXITCODE -eq 1) {
        return $true
    }

    throw "Unable to inspect /var/www/html/include/ost-config.php inside the container."
}

function Repair-OsTicketConfig {
    param(
        [string]$SecretSalt
    )

    Write-Step "Normalizing osTicket config file"
    & $script:DockerExe compose exec -T `
        -e "OST_LOCAL_SECRET_SALT=$SecretSalt" `
        -e "OST_LOCAL_ADMIN_EMAIL=$AdminEmail" `
        -e "OST_LOCAL_DBHOST=$DbHost" `
        -e "OST_LOCAL_DBNAME=$DbName" `
        -e "OST_LOCAL_DBUSER=$DbUser" `
        -e "OST_LOCAL_DBPASS=$DbPassword" `
        -e "OST_LOCAL_DBPREFIX=$TablePrefix" `
        osticket php /usr/src/osticket/configure_local_install.php

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to normalize /var/www/html/include/ost-config.php."
    }
}

Ensure-DockerDaemon
Set-Location $PSScriptRoot

if ($ResetData) {
    Write-Step "Removing existing containers and database volume"
    try {
        Invoke-Compose -Arguments @("down", "-v")
    }
    catch {
        Write-Host "Reset cleanup returned a non-zero exit code; continuing with a fresh build."
    }
}

Write-Step "Building and starting local osTicket stack"
Invoke-Compose -Arguments @("up", "-d", "--build")

Write-Step "Waiting for MySQL to become healthy"
Wait-Until -Description "MySQL health" -TimeoutSeconds 240 -DelaySeconds 5 -Condition {
    try {
        $status = & $script:DockerExe inspect --format "{{.State.Health.Status}}" osticket-mysql 2>$null
        return $status.Trim() -eq "healthy"
    }
    catch {
        return $false
    }
}

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$performedInstall = $false
$secretSalt = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')

if (-not (Test-OsTicketInstalled)) {
    Write-Step "Waiting for osTicket setup page"
    Wait-Until -Description "osTicket web app" -TimeoutSeconds 240 -DelaySeconds 5 -Condition {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8080/setup/install.php" -WebSession $session -UseBasicParsing -TimeoutSec 20
            return $response.StatusCode -ge 200 -and $response.StatusCode -lt 400
        }
        catch {
            return $false
        }
    }

    Write-Step "Running unattended osTicket installation"
    $body = @{
        s = "install"
        name = $HelpdeskName
        email = $SystemEmail
        lang_id = "en_US"
        fname = $AdminFirstName
        lname = $AdminLastName
        admin_email = $AdminEmail
        username = $AdminUsername
        passwd = $AdminPassword
        passwd2 = $AdminPassword
        prefix = $TablePrefix
        dbhost = $DbHost
        dbname = $DbName
        dbuser = $DbUser
        dbpass = $DbPassword
        timezone = "UTC"
    }

    $installResponse = Invoke-WebRequest -Uri "http://localhost:8080/setup/install.php" -Method Post -Body $body -WebSession $session -UseBasicParsing -TimeoutSec 180
    Repair-OsTicketConfig -SecretSalt $secretSalt
    Wait-Until -Description "installed osTicket admin page" -TimeoutSeconds 120 -DelaySeconds 5 -Condition {
        Test-OsTicketInstalled
    }
    $installed = Test-OsTicketInstalled
    $configResolved = Test-OsTicketConfigResolved
    if (-not $installed -or -not $configResolved) {
        $message = if ($installResponse.Content) { $installResponse.Content.Substring(0, [Math]::Min(1200, $installResponse.Content.Length)) } else { "No response body returned." }
        throw "Unattended osTicket installation did not complete successfully. Response excerpt:`n$message"
    }
    $performedInstall = $true
}
else {
    Write-Step "osTicket is already installed; skipping installer"
}

Write-Step "Finalizing container permissions"
& $script:DockerExe compose exec -T osticket sh -lc "rm -rf /var/www/html/setup && chmod 644 /var/www/html/include/ost-config.php"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to finalize osTicket permissions."
}

if ($ImportSampleTickets -and $performedInstall) {
    Write-Step "Creating sample tickets"
    & $script:DockerExe compose exec -T osticket php /usr/src/osticket/create_sample_tickets.php
    if ($LASTEXITCODE -ne 0) {
        throw "Sample ticket import failed."
    }
}
elseif ($ImportSampleTickets) {
    Write-Step "Skipping sample ticket import because this instance was already installed"
}

if ($OpenBrowser) {
    Write-Step "Opening local URLs"
    Start-Process "http://localhost:8080/" | Out-Null
    Start-Process "http://localhost:8080/scp/" | Out-Null
    Start-Process "http://localhost:8081/" | Out-Null
}

Write-Step "Installation complete"
Write-Host "User portal : http://localhost:8080/"
Write-Host "Admin panel : http://localhost:8080/scp/"
Write-Host "phpMyAdmin  : http://localhost:8081/"
Write-Host "Username    : $AdminUsername"
Write-Host "Password    : $AdminPassword"
Write-Host "Admin email : $AdminEmail"