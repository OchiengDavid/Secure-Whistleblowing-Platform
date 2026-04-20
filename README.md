# SafeReport App

A secure, anonymous report submission platform that automatically strips metadata from uploaded files to protect user privacy.

## Features

- **Anonymous Submissions**: Users can submit reports without identifying information
- **Metadata Stripping**: Automatically removes EXIF data and metadata from uploaded files
  - Supports: JPG, PNG, TIFF (EXIF removal)
  - Other formats: Metadata preserved (encryption provides additional protection)
- **End-to-End Encryption**: Files are encrypted using NaCl cryptography
  - Public key encryption ensures only authorized admins can decrypt files
  - Zero-knowledge encryption - server cannot decrypt files without private key
- **Secure Storage**: Reports and encrypted files stored securely in the database
- **Admin Interface**: Manage and review submitted reports with decryption capability
- **Tor Integration**: Can be deployed as a hidden service (.onion address)

## Project Structure

```
safe_report_app/
├── safereport_project/   ← Django project configuration
├── reports/              ← Main app with models, views, templates
│   ├── migrations/
│   ├── templates/reports/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   └── admin.py
├── static/               ← CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
├── media/                ← User uploads (gitignored)
├── SRS/                  ← Software Requirements Specification
├── venv/                 ← Virtual environment (gitignored)
├── manage.py
├── db.sqlite3            ← SQLite database (gitignored)
├── requirements.txt      ← Python dependencies
└── README.md
```

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd safe_report_app
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate encryption keys
```bash
python generate_keys.py
```

This will generate public/private key pairs for encrypting files. Save the output securely.

### 5. Configure environment variables
Create a `.env` file or set environment variables:
```bash
OFFICER_PUBLIC_KEY=your_public_key_here
OFFICER_PRIVATE_KEY=your_private_key_here
```

### 6. Apply database migrations
```bash
python manage.py migrate
```

### 7. Create admin user
```bash
python manage.py createsuperuser
```

## Running the Application

### Development Server
```bash
python manage.py runserver 8000
```

Access the app at: `http://127.0.0.1:8000`

### Admin Interface
```
http://127.0.0.1:8000/admin/
```
Login with your superuser credentials.

## Tor Hidden Service Setup

### 1. Install Tor (if not already installed)
```bash
sudo apt-get install tor
```

### 2. Configure Tor (`/etc/tor/torrc`)
Add the following lines:
```
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8000
```

### 3. Restart Tor
```bash
sudo systemctl restart tor
```

### 4. Get your .onion address
```bash
sudo cat /var/lib/tor/hidden_service/hostname
```

### 5. Access via Tor Browser
Open Tor Browser and navigate to the `.onion` address obtained in step 4.

## Dependencies

- **Django 6.0.4**: Web framework
- **Pillow 12.2.0**: Image processing (EXIF removal)
- **PyNaCl 1.5.0**: Cryptography library for end-to-end encryption
- **psycopg2-binary 2.9.11**: PostgreSQL adapter
- **SQLparse 0.5.5**: SQL parser utility
- **ExifTool**: External tool for comprehensive metadata removal

## Database Models

### AnonymousReport
- `subject` (CharField, max 200 chars): Report title
- `content` (TextField): Report content
- `attachment` (FileField): Uploaded file
- `submitted_at` (DateTimeField): Submission timestamp

## Security Considerations

- ✅ Metadata automatically stripped from all uploads
- ✅ Anonymous submission (no user authentication required)
- ✅ Admin interface requires Django superuser authentication
- ✅ Tor hidden service support for maximum anonymity
- ⚠️ Database should be encrypted in production
- ⚠️ Use HTTPS/TLS in production environments
- ⚠️ Configure proper Django security settings (DEBUG=False in production)

## File Format Support

### Image Files
- JPG / JPEG
- PNG
- TIFF

### Other Formats (via ExifTool)
- PDF
- DOC / DOCX
- MP4 / MOV
- And many more...

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
python manage.py runserver 8001  # Use a different port
```

### Tor Hidden Service Not Working
1. Check Tor is running: `sudo systemctl status tor`
2. Verify configuration: `grep -A 2 'HiddenService' /etc/tor/torrc`
3. Check Django is accessible locally: `curl http://127.0.0.1:8000`
4. Restart Tor: `sudo systemctl restart tor`

### Database Issues
Reset database (WARNING: deletes all data):
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit a pull request

## License

This project is provided as-is. Use at your own risk.

## Support

For issues or questions, contact the development team.
