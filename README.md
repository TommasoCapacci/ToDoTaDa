# ToDoTaDa

ToDoTaDa is a simple web application (available [here](https://todotada.pythonanywhere.com/)) built with Flask that allows users to manage their to-do lists. Users can register, log in, create, edit, mark as done, and delete tasks.

This project was inspired by the need for a simple and effective to-do list application.

## Features

- **User Authentication**: Users can register, log in, and log out securely.
- **Todo Management**: Users can create new tasks, edit existing tasks, mark tasks as done, and delete tasks.
- **Filter and Sorting**: Users can filter tasks by keywords and sort tasks by completion status.
- **Responsive Design**: The application is designed to work well on both desktop and mobile devices.

## Technologies Used

- **Flask**: Python web framework used for backend development.
- **Flask-WTF**: Flask extension for handling forms.
- **Flask-SQLAlchemy**: Flask extension for database management.
- **Flask-Mail**: Flask extension for email sending functionality.
- **HTML/CSS**: Frontend design and layout.
- **JavaScript**: Used for client-side interactivity.

## Getting Started

To run ToDoTaDa locally, follow these steps:

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the database by running `python manage.py db upgrade`.
4. Set the necessary environment variables for Flask-Mail (if using email functionality).
5. Run the application using `python manage.py run`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.