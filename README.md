---
title: Youtube QA
emoji: 🐨
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 3.50.2
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Project Name

## Setting up Python Environment

1. Install Python: Download and install Python from the [official website](https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during the installation.

2. Verify Python Installation: Open a new terminal window and run the command `python --version`. You should see Python's version number.

3. Install Virtualenv: Run the command `pip install virtualenv` to install the virtualenv package. This package allows you to create isolated Python environments.

4. Create a New Virtual Environment: Navigate to your project directory and run the command `python -m venv env` to create a new virtual environment in a folder named "env".

5. Activate the Virtual Environment: Run the command `source env/bin/activate` (on Linux/macOS) or `.\env\Scripts\activate` (on Windows) to activate the virtual environment.

## Installing Dependencies

This project requires the following dependencies:

- pytube
- openai

To install these dependencies, run the command `pip install -r requirements.txt` in your terminal.

## Running the Application

After setting up your environment and installing dependencies, you can run the application with the command `python app.py`.
