# Books-FastAPI

A modern web application built with FastAPI for managing books. This project demonstrates a robust backend architecture with authentication, admin controls, and book management capabilities.

## Features

- RESTful API for book management
- User authentication system
- Admin panel with advanced controls
- Database migrations using Alembic
- Docker containerization
- Clean and organized project structure

## Getting Started

### Prerequisites

- Python 3.8+
- Docker
- Node.js (for frontend development)
- Modern web browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Books-FastAPI.git
cd Books-FastAPI
```

2. Set up the database:
```bash
alembic upgrade head
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
uvicorn main:app --reload
```

### Accessing the Application

- API Documentation: http://localhost:8000/docs
- Application: http://localhost:8000

## Project Structure

```
Books-FastAPI/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── books.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       └── login.html
├── static/
│   ├── css/
│   │   ├── base.css
│   │   └── bootstrap.css
│   ├── js/
│   │   ├── base.js
│   │   ├── bootstrap.js
│   │   ├── jquery-slim.js
│   │   └── popper.js
│   └── img/
│       └── favicon.svg
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── database.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please:

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Md Jiyaul Haq - Main Developer
