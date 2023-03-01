# Basic CRUD Api example
... using [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/)

## Goal

* Efficiently create Rest APIs
* Use what you know = Python
* Have a nice documentation (Swagger UI)

## Getting startet

* create .env file:
  ```
  DATABASE_DIALECT=sqlite
  DATABASE_NAME=app.db
  ```
  
* install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
   
* run app:
  ```bash
  uvicorn app.main:app --reload
  ```

* go to url printed to console: http://127.0.0.1:8000
