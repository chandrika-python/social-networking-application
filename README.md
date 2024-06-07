# Django REST API Project(social_networking_project)

## Installation Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/chandrika-python/social_networking.git
    cd social_networking_api
    ```

2. **Set up a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

## Docker Setup

1. **Build and start the containers:**
    ```sh
    docker-compose up --build
    ```

2. **Apply migrations in the Docker container:**
    ```sh
    docker-compose exec web python manage.py migrate
    ```

3. **Create a superuser in the Docker container:**
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## Postman Collection

- [Postman Collection](path/to/your/postman/collection)

## Endpoints

1. **Register:** `/register/`
2. **Login:** `/login/`
3. **Logout:** `/logout/`
3. **User Search:** `/search-users/`
4. **Send Friend Request:** `/friend-requests/send/`
5. **Accept Friend Request:** `/friend-requests/<int:pk>/accept/`
6. **Reject Friend Request:** `/friend-requests/<int:pk>/reject/`
7. **List Friends:** `/friends/`
8. **List Pending Friend Requests:** `/pending-requests/`
