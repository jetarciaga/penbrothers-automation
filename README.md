# Automation: Downloading, Merging, Extracting CSV and Uploading via SFTP

This is a python project to showcase automation using Python, Selenium and Paramiko python package.

## Introduction

This project demonstrates how to perform web automation using selenium, pandas to merge csv files, and paramiko to upload via sftp.

## Features

- Navigate and login to a website.
- Interact with elements (e.g., copy text, filling forms, and clicking buttons)
- Download file
- Headless browser option for running without a GUI
- Working with csv files (e.g., merging, adding columns)
- Navigating directoris
- Working with files (e.g., creating, transforming, and deleting files)
- Uploading file via sftp

## Getting Started

### Prerequisites

- Python 3:11:4 installed
- Firefox browser installed
- Webdriver for Firefox (included in the project)
- GitBash if using windows

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jetarciaga/penbrothers-automation.git
   cd penbrothers-automation
   ```

2. Create virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate virtual environment:

   Windows:

   ```bash
   .\\.venv\\Scripts\\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create neccessary folders (e.g., assets, logs, outputs) inside the app folder

## Usage

1. Change directory:

   ```bash
   cd app
   ```

2. Run the automation script:

   ```bash
   python main.py
   ```

## License

Copyright © 2023 [Jethro Arciaga](https://www.linkedin.com/in/jethroarciaga/).

This project [MIT](https://github.com/jetarciaga/penbrothers-automation/blob/main/LICENSE) licensed
