import os
import django
import sys


def setup_users():
    """
    Reads username/password pairs from environment variables and creates a Django superuser
    and a regular user.  Handles potential errors during user creation.
    """
    # Determine the project directory
    manage_py_dir = os.path.dirname(os.path.abspath(__file__))
    # Add the project directory to the Python path
    sys.path.append(manage_py_dir)

    # Set up Django environment (assuming this script is in your Django project root)
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "task.settings"
    )  # Replace with your project name
    django.setup()

    from django.contrib.auth.models import User
    from django.core.management import call_command
    from django.db.utils import IntegrityError

    # Environment variable names
    superuser_username = "admin"
    superuser_password = "Hello$123"
    testuser_username = "test"
    testuser_password = "Hello$123"

    try:
        # Create superuser
        if not User.objects.filter(username=superuser_username).exists():
            User.objects.create_superuser(
                username=superuser_username, password=superuser_password
            )
            print(f"Superuser '{superuser_username}' created successfully.")
        else:
            print(f"Superuser '{superuser_username}' already exists.")

    except IntegrityError as e:
        print(f"Error creating superuser: {e}")
        print("This likely means the username is already taken.")

    try:
        # Create test user
        if not User.objects.filter(username=testuser_username).exists():
            User.objects.create_user(
                username=testuser_username, password=testuser_password
            )
            print(f"Test user '{testuser_username}' created successfully.")
        else:
            print(f"Test user '{testuser_username}' already exists.")
    except IntegrityError as e:
        print(f"Error creating test user: {e}")
        print("This likely means the username is already taken.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    setup_users()
    fetch_and_store_countries()
