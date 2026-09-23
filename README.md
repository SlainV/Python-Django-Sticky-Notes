# Sticky Notes

A simple web-based Sticky Notes application built with Django. Users can create, view, edit, and delete notes through an easy-to-use interface.

## Features

- Create new sticky notes
- View all notes on a single page
- Edit existing notes
- Delete notes
- Choose a custom note colour
- Simple and clean user interface

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite (default Django database)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SlainV/Python-Django-Sticky-Notes.git
cd sticky-notes
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Open the application

Visit:

```
http://127.0.0.1:8000/
```

## Project Structure

```text
sticky_notes/
│
├── notes/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── tests.py
│   └── templates/
│
├── manage.py
└── requirements.txt
```

## Testing

Run all tests:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test notes
```

## Future Improvements

Possible enhancements include:

- User authentication
- Search and filtering
- Note categories
- Note archiving
- Rich text formatting
- API support

## Author

Developed as part of a Django learning project.

## License

This project is provided for educational purposes.