# Welcome to Country Explorer

## Project Layout

```
requirements.txt     # Dependency installation
server/
    task/            # Django project
    countries/       # Django app for country data
    api/             # Django app for REST API
    ...              # Other markdown pages, images, and static files
```

# Django Country Data Project Documentation

This document provides a comprehensive guide to setting up, running, and using the Django Country Data Project. This project leverages the REST Countries API to fetch and store country information, presenting it through a user-friendly Django web application.

## Table of Contents

- [Welcome to Country Explorer](#welcome-to-country-explorer)
  - [Project Layout](#project-layout)
- [Django Country Data Project Documentation](#django-country-data-project-documentation)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Author Information](#2-author-information)
  - [3. Technical Details](#3-technical-details)
  - [4. Prerequisites](#4-prerequisites)
  - [5. Setup and Installation](#5-setup-and-installation)
  - [6. Accessing the Application](#6-accessing-the-application)
  - [🚀 Run the Code Fusion App with Docker](#-run-the-code-fusion-app-with-docker)
    - [🐳 Pull the Docker Image](#-pull-the-docker-image)
    - [▶️ Run the Container](#️-run-the-container)
    - [🌐 Access the App](#-access-the-app)

## 1. Introduction

The Django Country Data Project is designed to provide a simple and efficient way to access and display information about countries. It automates the process of retrieving data from the REST Countries API and stores it in a local database, making it easily accessible through a Django-powered web interface.

## 2. Author Information

!!! info "About Author"
    **Developed as part of the Code Fusion AI Python Developer Assignment (May 2025).**

    - **Author:** `Nazmul Alam Diptu ` 
    - **Contact:** `diptunazmulalam@gmail.com`

## 3. Technical Details


!!! info "**Backend:**"
  - **Framework:** `Django`  
  - **API Development:** `Django REST Framework  `
  - **Database:** `SQLite`  
  - **Authentication:** `JWT (JSON Web Tokens) ` 
  - **API Security:** `Django Rest HROTTLE_RATES ` 

!!! info "**Frontend:**"
  - **Templating:** `Django Templates  `
  - **Styling:** `Bootstrap 5  `

!!! info "**Data Source:**"

- **API:** `REST Countries API v3.1  `
- **API Documentation:** `OpenAPI / ReDoc`  

## 4. Prerequisites

Ensure the following are installed on your system:

- **Python 3.12**  
  Verify with `python --version` or `python3 --version`.

- **Git**  
  Required to clone the repository.

## 5. Setup and Installation

!!! info "Setup and Installation Steps"

    Follow these steps to set up the project locally:

    ### 5.1. Clone the Repository

    ```bash
    git clone https://github.com/diptu/code-Fusion-AI
    cd code-Fusion-AI
    ```

    ### 5.2. Create and Activate a Virtual Environment

    #### On macOS and Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    #### On Windows:
    ```bash
    python -m venv venv
    .\env\Scripts\activate
    ```

    ### 5.3. Install Dependencies

    ```bash
    cd server/task
    pip install -r requirements.txt
    ```
   
   - Open the Django shell:
  
    ```bash
    python manage.py shell
    ```

    ### 5.4. Apply Database Migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    ### 5.5. Fetch and Store Country Data

    Open the Django shell:
    - Inside the shell, run the following:
    - Will create a sueruser with username `admin` & password `Hello$123` and
    - one reqular with username `test` & password `Hello$123`

    ```bash
    from utils import setup_users
    setup_users()
    ```

    Then run the following inside the shell to fetch the data from the API and store it in the database:

    ```py
    from countries.utils import fetch_and_store_countries
    fetch_and_store_countries()
    ```

    Exit the shell after completion:

    ```py
    exit()
    ```

    ### 5.6. Start the Django Development Server

    ```bash
    python manage.py runserver
    ```

    Visit `http://127.0.0.1:8000/` in your browser to access the application.

## 6. Accessing the Application

!!! success "Accessing the Application"
    Once the server is running, open your browser and navigate to:

    ```bash
    http://127.0.0.1:8000/
    ```

    You’ll see the main interface of the Django Country Data Project. From here, you can explore, search, and view detailed country information.


## 🚀 Run the Code Fusion App with Docker
### 🐳 Pull the Docker Image
To fetch the latest public image from Docker Hub:
```bash
docker pull diptu/code_fusion_img:latest
```
### ▶️ Run the Container
> To start the application:

```bash
docker run -d --name code_fusion -p 8000:8000 diptu/code_fusion_img:latest
```

###  🌐 Access the App
Once the container is running, open your browser and visit:

```bash
http://localhost:8000
```
Now you can access the project at `http://127.0.0.1:8000/` in your browser.

###🛑 Stop and Remove the Container
-To stop and remove the container when you're done:

```bash
docker stop code_fusion && docker rm code_fusion
```
