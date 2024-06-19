# Fresh-Hub

Fresh-Hub is a command-line application that retrieves information of a GitHub user and creates or updates a contact in Freshdesk. Optionally, it can persist the GitHub user's information in a relational database.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Program](#running-the-program)
- [Testing](#testing)


## Requirements

1. **GitHub Account:** You need a GitHub account to generate a personal access token. Follow [this guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to create one.

2. **Freshdesk Account:** You need a Freshdesk account to obtain your subdomain and API key. Follow [this guide](https://support.freshdesk.com/en/support/solutions/articles/215517-how-to-find-your-api-key) to get your API key.

3. **Python 3.11:** Ensure you have Python 3.11 installed. You can download it from [python.org](https://www.python.org/downloads/release/python-3110/).

## Installation

### Windows

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/Fresh-Hub.git
    cd Fresh-Hub
    ```

2. **Install Python:**
    Ensure Python 3.11 is installed. You can download it from [python.org](https://www.python.org/downloads/release/python-3110/).

3. **Create and activate a virtual environment:**
    ```sh
    python -m venv env
    env\Scripts\activate
    ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Ubuntu

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/Fresh-Hub.git
    cd Fresh-Hub
    ```

2. **Install Python and required libraries:**
    ```sh
    sudo apt update
    sudo apt install python3.11 python3.11-venv python3.11-dev mariadb-server libmariadb3 libmariadb-dev
    ```

3. **Create and activate a virtual environment:**
    ```sh
    python3.11 -m venv env
    source env/bin/activate
    ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### macOS

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/Fresh-Hub.git
    cd Fresh-Hub
    ```

2. **Install Python and required libraries:**
    - Install Homebrew if you haven’t already: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    - Install Python and MariaDB: `brew install python@3.11 mariadb`

3. **Create and activate a virtual environment:**
    ```sh
    python3.11 -m venv env
    source env/bin/activate
    ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```


## Setup

1. **Configure environment variables**:
    Create a `.env` file in the root directory of the project with the following content:
    ```dotenv
    GITHUB_TOKEN=your_github_token
    FRESHDESK_TOKEN=your_freshdesk_token
    # Optional database configuration
    # DB_USER=your_db_user
    # DB_PASSWORD=your_db_password
    # DB_HOST=your_db_host
    # DB_PORT=your_db_port
    # DB_NAME=your_db_name
    ```

    Replace the placeholders with your actual values.

2. **OPTIONAL: Use `database_structure.sql` to create your database:**

    Open MySQL Workbench or any other database management tool, and run the provided SQL script to create the necessary table in your database. 

    To execute the script in MySQL Workbench:
    
    - Open MySQL Workbench and connect to your database.
    - Open a new SQL tab and load the `database_structure.sql` file.
    - Execute the script to create the table.

## Running the Program

To run the program, use the following command:

```sh
    python main.py <github_username> <freshdesk_subdomain>
```

**Samples**
- <github_username>: The GitHub username of the user whose information you want to fetch.
- <freshdesk_subdomain>: The subdomain of your Freshdesk account.

```sh
    python main.py gosho goshocompany
```

## Testing

**To run the unit tests, use the following command:**

```sh
    python -m unittest discover -s tests
```

**This will discover and run all the unit tests in the tests directory. These tests cover various scenarios to ensure the functionality of the application.**





