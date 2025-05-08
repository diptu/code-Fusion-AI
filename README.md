# Django Country Data Project

This project fetches and stores country data using the REST Countries API and presents it in a Django application.

## Setup and Run the Project

Follow the steps below to run the project locally.

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/diptu/code-Fusion-AI
cd code-Fusion-AI
```
## Create and Activate a Virtual Environment
- Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```
## Install Dependencies
- Install the required dependencies:

```bash
pip3 install -r requirements.txt
```
## Apply Database Migrations
- Apply the migrations to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```
## Fetch and Store Country Data
To fetch and store country data, run the Django shell:
```bash
python manage.py shell
```
### Inside the shell, run the following:
  - Will create a sueruser with username `admin` & password `Hello$123` and
  - one reqular with username `test` & password `Hello$123`

```bash
from utils import setup_users
setup_users()
```


```bash
from countries.utils import fetch_and_store_countries
fetch_and_store_countries()
```
##Start the Django Development Server
- Start the Django development server:

```bash
python manage.py runserver
```
Now you can access the project at `http://127.0.0.1:8000/` in your browser.