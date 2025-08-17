# Genealogy Application

A command-line application for managing family tree data, built with Python and MySQL.

## Features

- Add and manage people in the family tree
- Create family relationships (parent-child, spouse, sibling)
- Search for people by name
- View family trees
- Generate reports on relationships and locations
- Secure database connection with environment variables

## Prerequisites

- Python 3.7+
- MySQL 8.0+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sbd_proj_2p
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your database:
   - Create a MySQL database named `familysearch`
   - Import the database schema from `squema.sql`

4. Configure the application:
   - Copy `.env.example` to `.env`
   - Update the database credentials in `.env`

## Configuration

Edit the `.env` file with your database credentials:

```
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=familysearch
DB_USER=your_username
DB_PASSWORD=your_password

# Application Settings
DEBUG=True
```

## Usage

Run the application:

```bash
python genealogy_app.py
```

### Menu Options

1. **Add a new person** - Add someone to the family tree
2. **Add a family relationship** - Connect family members
3. **Search people** - Find people by name
4. **View family tree** - Display a person's family tree
5. **View relationships report** - See all relationships
6. **View people by location** - Group people by birth location
0. **Exit** - Quit the application

## Database Schema

The application uses the following main tables:

- `Personas` - Stores individual people
- `Relaciones_Familiares` - Stores family relationships
- `Usuarios` - Application users
- `Registros_Historicos` - Historical records
- `Recuerdos` - Photos and documents
- `Amistades` - User friendships

## Security

- Database credentials are stored in `.env` (not in version control)
- Passwords are hashed before storage
- Input validation is performed on all user inputs

## Troubleshooting

- **Connection issues**: Verify your database credentials in `.env`
- **Database errors**: Make sure the database is running and the schema is imported
- **Python errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## License

This project is licensed under the MIT License - see the LICENSE file for details.