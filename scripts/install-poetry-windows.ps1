# Set Execution Policy for Current User
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Install Scoop
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# Install pipx via Scoop
scoop install pipx

# Set up pipx environment variables
pipx ensurepath

# Install Poetry via pipx
pipx install poetry
