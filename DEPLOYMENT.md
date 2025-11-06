# Production Deployment Guide

This guide covers deploying the Hostel Management System securely in a production environment.

## Pre-Deployment Security Checklist

### 1. Environment Configuration
- [ ] Create production `.env` file with secure credentials
- [ ] Generate strong Flask secret key (32+ characters)
- [ ] Use dedicated database user with minimal privileges
- [ ] Set `FLASK_DEBUG=False` in production

### 2. Database Security
- [ ] Create dedicated MySQL user for the application
- [ ] Grant only necessary permissions (SELECT, INSERT, UPDATE, DELETE)
- [ ] Use strong database passwords
- [ ] Enable MySQL SSL if possible

### 3. Application Security
- [ ] Change all default passwords
- [ ] Remove or secure sample user accounts
- [ ] Review and update admin credentials
- [ ] Enable HTTPS/SSL certificates

## Production Environment Setup

### 1. Create Database User
```sql
-- Connect to MySQL as root
CREATE USER 'hostel_app'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT SELECT, INSERT, UPDATE, DELETE ON student_hostel.* TO 'hostel_app'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Production Environment Variables
```bash
# Production .env file
FLASK_SECRET_KEY=your-very-secure-32-character-secret-key-here
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_USER=hostel_app
DB_PASSWORD=secure_database_password_here
DB_NAME=student_hostel
DB_CHARSET=utf8mb4
```

### 3. Web Server Configuration

#### Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

#### Using Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### 1. Application Logging
```python
# Add to app.py for production logging
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/hostel_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 2. Database Backup
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u hostel_app -p student_hostel > /backups/hostel_db_$DATE.sql
find /backups -name "hostel_db_*.sql" -mtime +7 -delete
```

## Performance Optimization

### 1. Database Indexing
```sql
-- Add indexes for better performance
CREATE INDEX idx_student_id ON pass_requests(student_id);
CREATE INDEX idx_request_date ON pass_requests(request_date);
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_student ON attendance(student_id, date);
```

### 2. Application Caching
```python
# Consider adding Flask-Caching for session data
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

## Security Hardening

### 1. Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. Regular Updates
```bash
# Keep system updated
sudo apt update && sudo apt upgrade

# Update Python packages
pip install --upgrade -r requirements.txt
```

### 3. Security Headers
```python
# Add security headers to Flask app
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## Backup and Recovery

### 1. Database Backup
- Schedule daily automated backups
- Test backup restoration regularly
- Store backups in secure, off-site location

### 2. Application Backup
- Backup application files and configuration
- Version control with Git
- Document deployment procedures

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Check credentials and network connectivity
2. **Permission Denied**: Verify file permissions and user privileges
3. **SSL Certificate Issues**: Check certificate validity and renewal
4. **Performance Issues**: Monitor database queries and server resources

### Log Locations
- Application logs: `/var/log/hostel_app/`
- Nginx logs: `/var/log/nginx/`
- MySQL logs: `/var/log/mysql/`

## Support and Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check database performance
- [ ] Update security patches
- [ ] Backup verification
- [ ] SSL certificate renewal

### Emergency Contacts
- Database Administrator: [contact-info]
- System Administrator: [contact-info]
- Application Developer: [contact-info]