# Load environment variables from .secrets file
# Run this with: . .\load_env.ps1

Write-Host "Loading environment variables from .secrets file..." -ForegroundColor Green

Get-Content .secrets | ForEach-Object {
    $line = $_.Trim()
    
    # Skip empty lines and comments
    if ($line -eq "" -or $line.StartsWith("#")) {
        return
    }
    
    # Parse KEY=VALUE
    if ($line -match "^([^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        # Set environment variable for current session
        [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
        
        Write-Host "Loaded: $key" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "Environment variables loaded successfully!" -ForegroundColor Green
Write-Host "You can now run Django commands" -ForegroundColor Yellow
