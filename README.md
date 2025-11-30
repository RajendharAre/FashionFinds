# Fashion Finds

Fashion Finds is an e-commerce platform built with Flask that allows users to browse, purchase, and manage fashion products.

## Features
- User authentication (registration, login, logout)
- Product browsing by category
- Shopping cart functionality
- Wishlist management
- Order placement and tracking
- Admin dashboard for product management
- Delivery agent dashboard
- Data visualization for admin analytics

## Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

## Environment Variables

Create a `.env` file in the root directory based on the `.env.example` file:

```bash
cp .env.example .env
```

Then update the values in the `.env` file with your own configuration.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Fashion-Finds-main
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```bash
   flask db upgrade
   ```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your web browser and navigate to `http://localhost:5000`

   The application should now be running and accessible at this address.

## Project Structure
```
Fashion-Finds-main/
├── app/                 # Main application package
│   ├── templates/       # HTML templates
│   ├── static/          # Static files (CSS, JS, images)
│   ├── __init__.py      # Application factory
│   ├── models.py        # Database models
│   ├── views.py         # Main routes
│   ├── auth.py          # Authentication routes
│   ├── admin.py         # Admin routes
│   ├── delivery.py      # Delivery agent routes
│   └── forms.py         # WTForms classes
├── instance/            # Database files
├── migrations/          # Database migration scripts
├── tests/               # Unit tests
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

## Testing
To run the tests:
```bash
python -m pytest tests/
```

## Database
The application uses SQLite as the database. The database file is located in the `instance/` directory.

## Troubleshooting

If you encounter issues with the virtual environment on Windows, you may need to set the execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License
This project is licensed under the MIT License.


## Run the project
To run the project, follow these steps:
- Use this command : `python main.py`