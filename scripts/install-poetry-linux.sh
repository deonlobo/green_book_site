#!/bin/bash

# Update package list
sudo apt update

# Install pipx
sudo apt install pipx

# Ensure pipx path
pipx ensurepath

# Install Poetry via pipx
pipx install poetry