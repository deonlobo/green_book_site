# Set Execution Policy for Current User
Write-Output '🔒  Setting execution policy for current user...'
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Install Scoop
Write-Output "🔍 Checking if Scoop is installed..."
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Output "📥  Installing Scoop..."
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

    # Check if Scoop installed correctly
    if (Get-Command scoop -ErrorAction SilentlyContinue) {
        Write-Output "✅  Scoop installed successfully."
    } else {
        Write-Output "❌  Scoop installation failed."
        exit 1
    }
} else {
    Write-Output "⚙️  Scoop is already installed. Skipping installation."
}

# Install pipx via Scoop
Write-Output "🔍  Checking if pipx is installed..."
if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
    Write-Output "📥  Installing pipx via Scoop..."
    scoop install pipx

    # Check if pipx installed correctly
    if (Get-Command pipx -ErrorAction SilentlyContinue) {
        Write-Output "✅  pipx installed successfully."
    } else {
        Write-Output "❌  pipx installation failed."
        exit 1
    }
} else {
    Write-Output "⚙️  pipx is already installed. Skipping installation."
}

# Set up pipx environment variables
Write-Output "🔧  Setting up pipx environment variables..."
pipx ensurepath

# Check if pipx path is set correctly
$envPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
if ($envPath -like "*C:\Users\*\.local\bin*") {
    Write-Output "✅  pipx path set successfully."
} else {
    Write-Output "❌  Failed to set pipx path."
    exit 1
}

# Install Poetry via pipx
Write-Output "🔍  Checking if Poetry is installed..."
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Output "📥  Installing Poetry via pipx..."
    pipx install poetry

    # Check if Poetry installed correctly
    if (Get-Command poetry -ErrorAction SilentlyContinue) {
        Write-Output "✅  Poetry installed successfully."
    } else {
        Write-Output "❌  Poetry installation failed."
        exit 1
    }
} else {
    Write-Output "⚙️  Poetry is already installed. Skipping installation."
}


# Prevent the terminal from closing
Write-Output "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')