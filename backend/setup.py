from setuptools import setup, find_packages

setup(
    name="trustytrade",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "psycopg2-binary",
        "python-dotenv",
    ],
) 