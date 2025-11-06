# Hostel Management System

A comprehensive web-based hostel management system built with Flask and MySQL. This system provides separate dashboards for students, faculty, and administrators to manage hostel operations efficiently.

## Features

### Student Features
- **Registration & Login**: Secure student registration and authentication
- **Pass Requests**: Submit leave requests with reason and date range
- **Attendance Tracking**: Check-in and check-out functionality
- **Dashboard**: View pass request status and attendance history

### Faculty Features
- **Login & Dashboard**: Secure faculty authentication and overview
- **Pass Approval**: Review and approve/reject student pass requests
- **Attendance Monitoring**: View daily attendance summary for all students
- **Profile Management**: View and manage faculty profile

### Admin Features
- **Admin Dashboard**: Overview of system statistics
- **Student Management**: Add, edit, and delete student records
- **Faculty Management**: Add, edit, and delete faculty records
- **Profile Management**: View admin profile information

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL with PyMySQL connector
- **Frontend**: HTML templates with Bootstrap styling
- **Session Management**: Flask sessions for user authentication

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hostel-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` file with your database credentials:
     ```bash
     # Update these values with your actual database credentials
     DB_PASSWORD=your-actual-database-password
     FLASK_SECRET_KEY=your-secure-secret-key
     ```
   - Ensure MySQL server is running

4. **Setup Database**
   
   **Option 1: Using SQL file**
   ```bash
   mysql -u root -p < database.sql
   ```
   
   **Option 2: Using Python setup script**
   ```bash
   python setup_database.py
   ```

5. **Create Admin User (Optional)**
   ```bash
   python create_admin.py
   ```

## Running the Application

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the system**
   - Open your browser and navigate to `http://localhost:5000`
   - The application will automatically check database connectivity on startup

## Default Login Credentials

### Students
- **Student ID**: STU001, **Password**: password123
- **Student ID**: STU002, **Password**: password123
- **Student ID**: STU003, **Password**: password123

### Faculty
- **Faculty ID**: FAC001, **Password**: faculty123
- **Faculty ID**: FAC002, **Password**: faculty123

### Admin
- Create admin accounts through database or modify the setup script

## Project Structure

```
hostel-management-system/
├── app.py                 # Main Flask application
├── database.sql          # Database schema and setup
├── setup_database.py     # Python database setup script
├── requirements.txt      # Python dependencies
├── static/
│   └── css/              # CSS stylesheets
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── index.html        # Landing page
    ├── *_login.html      # Login pages for different user types
    ├── *_dashboard.html  # Dashboard pages
    ├── *_profile.html    # Profile pages
    └── manage_*.html     # Admin management pages
```

## Database Schema

### Tables
- **students**: Student information and credentials
- **faculty**: Faculty information and credentials
- **admin**: Administrator accounts
- **pass_requests**: Student leave requests and approval status
- **attendance**: Daily check-in/check-out records

## API Endpoints

### Authentication
- `GET/POST /student_login` - Student login
- `GET/POST /faculty_login` - Faculty login  
- `GET/POST /admin_login` - Admin login
- `GET /logout` - Logout (all user types)

### Student Routes
- `GET /student_dashboard` - Student dashboard
- `GET/POST /register` - Student registration
- `GET/POST /request_pass` - Submit pass request
- `GET /mark_attendance` - Mark attendance

### Faculty Routes
- `GET /faculty_dashboard` - Faculty dashboard
- `GET /faculty_profile` - Faculty profile
- `GET /approve_pass/<id>/<action>` - Approve/reject pass requests

### Admin Routes
- `GET /admin_dashboard` - Admin dashboard
- `GET /admin_profile` - Admin profile
- `GET /manage_students` - Student management
- `GET /manage_faculty` - Faculty management
- `GET/POST /add_faculty` - Add new faculty
- `GET/POST /edit_student/<id>` - Edit student details
- `GET/POST /edit_faculty/<id>` - Edit faculty details
- `GET /delete_student/<id>` - Delete student
- `GET /delete_faculty/<id>` - Delete faculty

## Security Features

- Session-based authentication
- Role-based access control
- SQL injection prevention using parameterized queries
- Password protection for all user accounts
- Environment variable configuration for sensitive data
- Secure secret key management
- Database credentials protection

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Change default passwords** - Update all sample passwords in production
3. **Use strong secret keys** - Generate secure Flask secret keys
4. **Database security** - Use dedicated database users with limited privileges
5. **HTTPS in production** - Always use HTTPS in production environments

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding HTML templates in `templates/`
3. Update database schema if needed
4. Test functionality across all user roles

### Database Modifications
1. Update `database.sql` with schema changes
2. Modify `setup_database.py` if needed
3. Update application code to handle new fields

## Troubleshooting

### Database Connection Issues
- Verify MySQL server is running
- Check database credentials in `app.py`
- Ensure `student_hostel` database exists

### Application Won't Start
- Run with `--skip-db-check` flag to bypass database validation
- Check Python dependencies are installed
- Verify port 5000 is available

### Template Not Found Errors
- Ensure all HTML files are in the `templates/` directory
- Check template names match route render calls

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed security and configuration guidelines.

### Quick Production Setup
1. Remove sample data: `python remove_sample_data.py`
2. Create admin user: `python create_admin.py`
3. Configure production environment variables
4. Set up SSL/HTTPS
5. Use a production WSGI server (Gunicorn)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.