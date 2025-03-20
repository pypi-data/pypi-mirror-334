# FastAPI Cookiecutter
**⚡ A Powerhouse Template for FastAPI Projects ⚡**

FastAPI Cookiecutter is a highly customizable Python template designed to kickstart your FastAPI applications with a production-ready structure. Perfect for developers who want a scalable, modular foundation without the setup grind.

---

## Key Features
- **Flexible Setup**: Choose between **PostgreSQL** or **SQLite** databases.
- **Optional Add-Ons**: Enable **Docker**, **Redis**, or **GitHub Actions CI/CD** with a single prompt.
- **Modular Design**: Prebuilt structure with routers, models, schemas, and services.
- **Testing Ready**: Built-in **Pytest** support for async testing.
- **Database Migrations**: Seamless integration with **Alembic** for schema management.
- **Health Checks**: Monitor your app’s status with a dedicated endpoint.

---

## Installation
Install FastAPI Cookiecutter via PyPI (assuming you publish it):

```bash
pip install fastapi-cookiecutter
```

### Requirements
- Python 3.11+
- Dependencies: `cookiecutter` (automatically installed via pip)

---

## Quick Start
After installation, generate a new FastAPI project:

```bash
fastapi-cookiecutter
```

Or use it directly from GitHub:

```bash
cookiecutter gh:Mohammad222PR/fastapi-cookiecutters
```

Answer the prompts to customize your project, and you’re good to go!

---

## Usage Examples
Here’s how to wield FastAPI Cookiecutter:

### Basic Project
Generate a simple FastAPI app with SQLite:
```bash
cookiecutter gh:Mohammad222PR/fastapi-cookiecutters
# Enter project_name="MyAPI", database="sqlite", use_docker="no", use_ci_cd="no"
```

### Full-Stack Setup
Create a loaded project with Postgres, Docker, and CI/CD:
```bash
cookiecutter gh:Mohammad222PR/fastapi-cookiecutters --no-input \
  project_name="MyAPI" database="postgres" use_redis="yes" use_docker="yes" use_ci_cd="yes"
```

Check the generated `README.md` for next steps!

---

## Configuration Options
When running the template, you’ll be prompted for:

| Option            | Description                                   | Choices/Default          |
|-------------------|-----------------------------------------------|--------------------------|
| `project_name`    | Name of your project                         | e.g., "MyAPI"            |
| `project_slug`    | Auto-generated project directory name        | Auto-filled              |
| `author`          | Your name                                    | e.g., "Your Name"        |
| `version`         | Project version                              | "0.1.0"                 |
| `description`     | Short project description                    | e.g., "A FastAPI app"   |
| `database`        | Database type                                | "postgres" / "sqlite"   |
| `use_redis`       | Include Redis support                        | "yes" / "no"            |
| `use_docker`      | Include Docker and Compose files             | "yes" / "no"            |
| `use_ci_cd`       | Include GitHub Actions CI/CD pipeline        | "yes" / "no"            |

---

## Why FastAPI Cookiecutter?
- **Speedy Setup**: From template to running app in under 5 minutes.
- **Custom Power**: Tailor your project with zero bloat.
- **Scalable Base**: Ready for small scripts or massive APIs.
- **Pro Features**: Everything you need, nothing you don’t.

---


## License
FastAPI Cookiecutter is licensed under the [MIT License](https://github.com/Mohammad222pr/fastapi-cookiecutter/blob/main/LICENSE). Use it, tweak it, share it—responsibly.

---

## Notes
- **Responsible Customization**: Only include what your project needs—keep it lean!
- **Feedback**: Got ideas? Open an issue on [GitHub](https://github.com/Mohammad222pr/fastapi-cookiecutter/issues)!

---