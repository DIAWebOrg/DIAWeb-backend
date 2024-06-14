<a name="top"></a>

# DIAWeb backend

![Django](https://img.shields.io/badge/Django-green?style=flat-square&logo=django&logoColor=white)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DIAWebOrg_DIAWeb-backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DIAWebOrg_DIAWeb-backend)
[![Django Tests](https://github.com/DIAWebOrg/DIAWeb-backend/actions/workflows/main.yaml/badge.svg)](https://github.com/DIAWebOrg/DIAWeb-backend/actions/workflows/main.yaml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-alpha-orange)

<details>  
<summary><b>Table of contents</b></summary>
  
1. [Introduction](#introduction)
2. [Project structure](#project-structure)
3. [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
4. [Installing Dependencies](#installing-dependencies)
5. [Running the Project](#running-the-project)
6. [Contact data](#contact-data)
7. [License](LICENSE.md)
</details>

## Introduction

DIAWeb is a web application that allows the user to calculate their risk of suffering diabetes, based on an artificial intelligence powered model. This project is the backend of it, i.e., the API that computes such risk based on a range of biochemical markers.

## Project structure

- `.github/`: Contains dependabot configuration along with workflow file
- `.idx/`: Contains the file to build the development environment using nix package manager
- `mysite/`: This directory contains the source code of the project
  - `mysite/`: Common Python files for all the apps, includings `settings.py` and `urls.py`
  - `myapp/`: App specific files, including test files, models, views and scripts to build and model the neural network
    - `keras/`: Tensoflow-Keras related scripts
    - `migrations/`: Database related scripts
    - `utils/`: Diverse utility files
  - `db.sqlite3`: Currently unused since the database is PostgreSQL
  - `manage.py`: Entry point to run the project.
- `.gitignore`: Folders not to include in the repository
- `LICENSE.md`: MIT license of the project
- `CODE_OF_CONDUCT.md`: Behavioural guidelines for contributors
- `README.md`: A briefing of the project and how to run it
- `SECURITY.md`: Briefing of the security policy
- `devserver.sh`: Boot file to run the project
- `init_supabase.py`: Script to initialize supabase database
- `requirements.txt`: List of Python dependencies of the project

## Setting Up a Virtual Environment

To create a virtual environment, navigate to the project directory and run the following command:

```bash
python3 -m venv venv
```

This will create a new virtual environment in a folder named `venv`.

To activate the virtual environment, use the following command:

On Windows:

```bash
venv\Scripts\activate
```

On Unix or MacOS:

```bash
source venv/bin/activate
```

## Installing Dependencies

Once the virtual environment is activated, you can install the project's dependencies using the `requirements.txt` file. Run the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages for this project.

## Running the Project

To run the project, navigate to `mysite/` and then run

```bash
python manage.py runserver
```

## Contact data

If you have any request or inquiry, feel free to contact me at [pabcabmar3@alum.us.es](mailto:pabcabmar3@alum.us.es)

<a href="#top">Back to Top</a>
