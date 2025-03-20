# Flask-StartProject

Flask-StartProject is a simple and efficient Python script that automates the initialization of a Flask project. It sets up a project directory, creates a virtual environment, installs dependencies, and generates essential files such as `requirements.txt` and `app` folder.

## Features
- Creates a new Flask project structure
- Sets up a virtual environment automatically
- Installs dependencies based on user preferences
- Supports loading dependencies from a configuration file (JSON)
- Provides options for Git initialization
- Generates a `requirements.txt` file
- Creates template based project structure

## Installation
No installation is required. Just download the script and run it using Python 3.

## Usage
Run the script with the following options:

```sh
flask-startproject <project_name> [options]
```

### Options
- `-t, --template` - Specifies scaffold template (e.g., `api or web`)
- `-d, --deps` - Specifies dependencies to install (e.g., `auth,db,migrate`)
- `-f, --from-file` - Loads dependencies from a JSON file
- `--all-deps` - Installs all available dependencies
- `--git-init` - Initializes a Git repository in the project folder
- `--requirements` - Generates a `requirements.txt` file

### Example
#### Creating a Flask project with authentication and database support:
```sh
flask-startproject my_project -t api -d auth,db --git-init --requirements
```

#### Creating a Flask project with all dependencies:
```sh
flask-startproject my_project --all-deps
```

## Default Dependencies

The script supports predefined dependencies categorized as follows:

| Category   | Packages |
|------------|------------------------------------------------|
| auth       | Flask-Security-Too                            |
| db         | Flask-SQLAlchemy                              |
| forms      | Flask-WTF                                     |
| migrate    | Flask-Migrate                                 |
| cache      | Flask-Caching                                 |
| mail       | Flask-Mailman                                 |
| validation | Marshmallow                                   |
| jobs       | Celery                                        |
| test       | pytest                                        |

## Generated scaffold

When you select a template 'api' or 'web', your project is created based on the chosen model.

## License
This project is licensed under the MIT License.