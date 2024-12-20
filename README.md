# URL Shortener Application

This is a Flask-based URL shortener application designed to provide a simple and scalable solution for shortening and managing URLs. The application includes authentication, rate limiting, and a database-backed implementation for handling users and URLs.

---

## Features

- **User Management**: Create, read, update, and delete users.
- **URL Management**: Shorten URLs, manage aliases, and track redirect metrics.
- **Authentication**: Basic authentication with hashed passwords.
- **Rate Limiting**: Limits requests per minute, hour, and day.
- **Database Support**: Uses SQLite by default, easily extendable to other databases.
- **Production-ready**: Compatible with Gunicorn for deployment.

---

## Project Structure

```plaintext
app/
├── dal/                # Data Access Layer
├── database/           # Database setup
├── models/             # Database models
├── resources/          # Flask-RESTful resources
├── tests/              # Test suite
├── utils/              # Utility functions
└── app.py              # Main application entry point
```

---

## Getting Started

### Prerequisites

- Works with Python 3.13.0+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/crossy-l/url-shortener.git
   cd url-shortener
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database (optional):
   ```bash
   python api.py --recreate-db
   ```

---

## Running the Application

### Local Development

Run the application locally:
```bash
python api.py
```
The app will be available at `http://127.0.0.1:5000`.

### Gunicorn Support

Run the application in production using Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:gunicorn_app
```
- `-w 4`: Specifies 4 worker processes.
- `-b 0.0.0.0:5000`: Binds to all network interfaces on port 5000.

---

## Testing the Application

### Running Tests

To run the test suite, execute:
```bash
pytest app/tests/
```

### Test Coverage

To measure test coverage, use:
```bash
pytest --cov=app app/tests/
```

---

## Configuration

You can configure the application using command-line arguments or environment variables.

### Command-Line Arguments
- `--recreate-db`: Recreate the database tables.
- `--cache-dir`: Path to the cache directory (default: `cache`).
- `--sql-db-path`: Path to the SQLite database (default: `database.db`).
- `--requests-per-day`: Number of requests allowed per day (default: `28800`).
- `--requests-per-hour`: Number of requests allowed per hour (default: `1200`).
- `--requests-per-minute`: Number of requests allowed per minute (default: `20`).
- `--cache-timeout`: Cache timeout in seconds (default: `86400`).

Arguments to specify host and port will follow, for now these are the prototype arguments.

### Example Configuration
```bash
python app.py --recreate-db --cache-dir /tmp/cache --sql-db-path mydb.sqlite
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

