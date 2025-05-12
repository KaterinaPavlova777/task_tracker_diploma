# Task Tracker

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/task-tracker.git
```

2. Navigate to the project directory:

```
cd task-tracker
```

3. Set up the environment variables:

```
cp .env.example .env
```

Then, update the `.env` file with your database credentials and other necessary settings.

4. Run the Docker command:

```
docker-compose up --build
```

The application should now be running at `http://localhost:8000`.

## Usage

The Task Tracker application provides the following functionality:

- **Task Management**: Users can create, view, update, and delete tasks. Tasks can have a parent-child relationship and
  can be assigned to different performers.
- **Task Status**: Tasks can have one of three statuses: `created`, `in_progress`, or `completed`.
- **User Management**: Administrators can manage user accounts, including creating, updating, and deleting users.
- **Access Control**: Users have different access levels, which determine their permissions within the application.

To use the application, you can interact with the provided API endpoints using a tool like Postman or cURL. The API
documentation is available at `http://localhost:8000/docs/` or `http://localhost:8000/redoc/`.

## API

The Task Tracker application provides the following API endpoints:

### Tasks

- `GET /tasks/`: List all tasks
- `GET /tasks/<int:pk>`: Retrieve a specific task
- `POST /tasks/create/`: Create a new task
- `PUT /tasks/update/<int:pk>`: Update an existing task
- `DELETE /tasks/delete/<int:pk>`: Delete a task
- `GET /tasks/important/`: List important tasks (tasks with `created` status and a parent task with `in_progress`
  status)

### Users

- `POST /users/register/`: Register a new user
- `GET /users/`: List all users
- `GET /users/<int:pk>`: Retrieve a specific user
- `PUT /users/update/<int:pk>`: Update an existing user
- `DELETE /users/delete/<int:pk>`: Delete a user
- `GET /users/tasks/`: List all users with their task counts
- `GET /users/candidate/`: List candidate users for important tasks

