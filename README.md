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
cd server/task
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
from countries.utils import fetch_and_store_countries
fetch_and_store_countries()
```
##Start the Django Development Server
- Start the Django development server:


Now you can access the project at `http://127.0.0.1:8000/` in your browser.

### 🚀 Run the Code Fusion App with Docker
  
 🐳 Pull the Docker Image
To fetch the latest public image from Docker Hub:

```bash
docker pull diptu/code_fusion_img:latest
```

▶️ Run the Container
- To start the application:

```bash
docker run -d \
  --name code_fusion \
  -p 8000:8000 \
  diptu/code_fusion_img:latest
```
Now you can access the project at `http://127.0.0.1:8000/` in your browser.

### 🛑 Stop and Remove the Container
-To stop and remove the container when you're done:

```bash
docker stop code_fusion && docker rm code_fusion
```
