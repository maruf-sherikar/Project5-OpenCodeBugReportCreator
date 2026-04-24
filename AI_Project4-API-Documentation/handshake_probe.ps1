# AI Documentation Agent - Handshake Probe (Phase 2: LINK)
# This script verifies environmental readiness and integration connectivity.

$dotEnvFile = ".env"

if (-not (Test-Path $dotEnvFile)) {
    Write-Host "[ERROR] .env file not found. Please create one from .env.template." -ForegroundColor Red
    exit 1
}

# Simple .env parser for PowerShell
$envVars = @{}
Get-Content $dotEnvFile | ForEach-Object {
    if ($_ -match "^([^#\s][^=]*)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

Write-Host "--- LINK Phase: Integration Handshake ---" -ForegroundColor Cyan

# 1. Postman Connectivity
if ($envVars.ContainsKey("POSTMAN_API_KEY") -and $envVars["POSTMAN_API_KEY"] -ne "your_postman_api_key_here") {
    Write-Host "[LINK] Verifying Postman API Connection..." -NoNewline
    try {
        $headers = @{ "X-Api-Key" = $envVars["POSTMAN_API_KEY"] }
        $response = Invoke-RestMethod -Uri "https://api.getpostman.com/me" -Headers $headers -Method Get
        Write-Host " [SUCCESS]" -ForegroundColor Green
        Write-Host "       Authenticated as: $($response.user.username)"
    } catch {
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host "       Error: $($_.Exception.Message)"
    }
} else {
    Write-Host "[SKIP] Postman API Key missing or default values detected." -ForegroundColor Yellow
}

# 2. GitHub Connectivity
if ($envVars.ContainsKey("GITHUB_TOKEN") -and $envVars["GITHUB_TOKEN"] -ne "your_github_token_here") {
    Write-Host "[LINK] Verifying GitHub Token..." -NoNewline
    try {
        $headers = @{ "Authorization" = "token $($envVars["GITHUB_TOKEN"])"; "Accept" = "application/vnd.github.v3+json" }
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get
        Write-Host " [SUCCESS]" -ForegroundColor Green
        Write-Host "       Authenticated as: $($response.login)"
    } catch {
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host "       Error: $($_.Exception.Message)"
    }
} else {
    Write-Host "[SKIP] GitHub Token missing or default values detected." -ForegroundColor Yellow
}

Write-Host "-------------------------------------------"
if ($true) { Write-Host "[READY] LINK phase environment check complete." -ForegroundColor Green }
