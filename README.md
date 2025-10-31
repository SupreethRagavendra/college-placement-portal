# College Placement Training Portal

A comprehensive Laravel-based web application for managing college placement training programs with role-based authentication, email verification, and PostgreSQL database integration with Supabase.

## 🚀 Features

### Authentication & Authorization
- **Role-based Authentication**: Separate login/registration for Admin and Student roles
- **Email Verification**: Mandatory email verification before login
- **Secure Password Handling**: Laravel's built-in password hashing and validation
- **Session Management**: Secure session handling with remember me functionality

### Admin Features
- **Dashboard**: Comprehensive admin dashboard with statistics and quick actions
- **Student Management**: View and manage student accounts
- **Company Management**: Manage partner companies
- **Placement Tracking**: Track and manage placement records
- **Reports**: Generate placement and training reports

### Student Features
- **Personal Dashboard**: Track learning progress and achievements
- **Course Management**: View enrolled courses and assignments
- **Interview Scheduling**: View upcoming interviews
- **Certificate Management**: Download earned certificates
- **Progress Tracking**: Monitor learning progress and completion rates

### Technical Features
- **PostgreSQL Integration**: Full Supabase PostgreSQL database support
- **Email System**: SMTP-based email verification system
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Security**: CSRF protection, SQL injection prevention, XSS protection
- **Modern UI**: Beautiful gradient-based design with Font Awesome icons

## 🛠️ Technology Stack

- **Backend**: Laravel 12.x
- **Database**: PostgreSQL (Supabase)
- **Frontend**: Bootstrap 5, Font Awesome
- **Authentication**: Laravel Breeze
- **Email**: SMTP (configurable)
- **Server**: PHP 8.2+

## 📋 Prerequisites

- PHP 8.2 or higher
- Composer
- PostgreSQL driver for PHP (pdo_pgsql)
- Web server (Apache/Nginx) or Laravel development server

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd college-placement-portal
```

### 2. Install Dependencies
```bash
composer install
npm install
```

### 3. Environment Configuration
Copy the `.env.example` to `.env` and configure your environment variables:

```env
APP_NAME="College Placement Portal"
APP_ENV=local
APP_KEY=base64:your-app-key-here
APP_DEBUG=true
APP_URL=http://localhost:8000

# Database Configuration (Supabase PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=db.wkqbukidxmzbgwauncrl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD="Supreeeth24#"
DB_SSLMODE=require

# Email Configuration
MAIL_MAILER=smtp
MAIL_HOST=your-smtp-host
MAIL_PORT=587
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS="noreply@yourdomain.com"
MAIL_FROM_NAME="${APP_NAME}"
```

### 4. Generate Application Key
```bash
php artisan key:generate
```

### 5. Database Setup
```bash
# Run migrations
php artisan migrate

# Seed the database with admin user
php artisan db:seed --class=AdminSeeder
```

### 6. Start the Development Server
```bash
php artisan serve
```

The application will be available at `http://localhost:8000`

## 👥 Default Credentials

### Admin Account
- **Email**: admin@portal.com
- **Password**: Admin@123
- **Role**: Admin

### Student Account
- Students need to register through the registration form
- Email verification is required before login

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `email_verified_at`: Email verification timestamp
- `password`: Hashed password
- `role`: User role (admin/student)
- `remember_token`: Remember me token
- `created_at`, `updated_at`: Timestamps

### Email Verification Tokens Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `token`: Verification token
- `expires_at`: Token expiration time
- `created_at`, `updated_at`: Timestamps

## 🔐 Security Features

- **CSRF Protection**: All forms are protected with CSRF tokens
- **SQL Injection Prevention**: Using Eloquent ORM and prepared statements
- **XSS Protection**: Input sanitization and output escaping
- **Password Security**: Laravel's bcrypt hashing
- **Email Verification**: Prevents unauthorized account access
- **Role-based Access Control**: Middleware-based route protection

## 📧 Email Verification Process

1. User registers with email and role
2. System generates verification token
3. Verification email sent to user's email
4. User clicks verification link
5. Email is verified and user can login
6. Token expires after 1 hour

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Gradient backgrounds and smooth animations
- **Intuitive Navigation**: Clear sidebar navigation for both roles
- **Visual Feedback**: Loading states, success/error messages
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 🚀 Deployment

### Production Environment
1. Set `APP_ENV=production` and `APP_DEBUG=false`
2. Configure production database credentials
3. Set up proper SMTP email service
4. Configure web server (Apache/Nginx)
5. Set up SSL certificate
6. Configure queue workers for email processing

### Environment Variables for Production
```env
APP_ENV=production
APP_DEBUG=false
APP_URL=https://yourdomain.com

DB_CONNECTION=pgsql
DB_HOST=your-production-db-host
DB_PORT=5432
DB_DATABASE=your-production-db
DB_USERNAME=your-db-username
DB_PASSWORD=your-secure-password
DB_SSLMODE=require

MAIL_MAILER=smtp
MAIL_HOST=your-smtp-server
MAIL_PORT=587
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-email-password
MAIL_ENCRYPTION=tls
```

## 🧪 Testing

Run the test suite:
```bash
php artisan test
```

## 📝 API Endpoints

### Authentication Routes
- `GET /register` - Registration form
- `POST /register` - Process registration
- `GET /login` - Login form
- `POST /login` - Process login
- `POST /logout` - Logout user
- `GET /verify-email/{token}` - Email verification

### Protected Routes
- `GET /dashboard` - Redirect to role-based dashboard
- `GET /admin/dashboard` - Admin dashboard
- `GET /student/dashboard` - Student dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0** - Initial release with basic authentication and role management
- **v1.1.0** - Added email verification system
- **v1.2.0** - Enhanced UI/UX with modern design
- **v1.3.0** - Supabase PostgreSQL integration

---

**Note**: This application is designed for educational purposes and should be properly secured before production deployment.