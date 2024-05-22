# FastAPI skeleton-code
Skeleton Code of web framework that offers high performance and minimal boiler code for building APIs using **FastAPI**.

Already integrated with postgres using asynchronous library (**asyncpg**), **swagger** and production grade ASGI server using **Uvicorn**.

## Prerequisite:
`Python 3.6+`

## Getting Started
1. Clone this repo
2. create `.env` configuration file using `.env.example` as baseline
3. create python virtual environment
    ```
    python3 -m venv .venv
    source env/bin/activate
    ```
4. Install python library on requirements.txt
   ```
   pip -r requirements.txt
   ```
5. Testing can be initiated by using:
   ```
    pytest tests
   ```
6. Code coverage can be initiated by using:
   ```
   python -m coverage run {python_test_file}.py
   coverage report
   ```
7. Run web service on dev environment
   ```
    fastapi dev app/main.py
   ```
8. Swagger can be accesed on [http://localhost:8000/docs](http://localhost:8000/docs).

## Debbuger on VScode
Set *launch.json* as below:
* Conda
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Uvicorn",
            "type": "python",
            "request": "launch",
            "module": "app.main",
            "program": "/home/${USER}/anaconda3/envs/web/bin/uvicorn ${module}:app",
            "console": "integratedTerminal"
        }
    ]
}
```
* virtualenv
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Uvicorn",
            "type": "python",
            "request": "launch",
            "module": "app.main",
            "program": "${workspaceRoot}/venv/bin/uvicorn ${module}:app",
            "console": "integratedTerminal"
        }
    ]
}
```

## Project Structure
```--bash
$ tree -P '*.py|*.env|*.example' -a -I '.git|__pycache__|__init__.py|.empty|.pytest_cache|.vscode'

.
├── app
│   ├── main.py                     # Main application
│   ├── models                      # Schema location
│   │   ├── auth.py
│   │   └── response.py
│   ├── repository                  # Database crud
│   │   ├── role_mgmt.py
│   │   └── test_repository.py
│   ├── routes                      # APIs location
│   │   └── test_route.py
│   ├── services                    # Location of Business logic, adapter and DAO
│   │   ├── authentication.py
│   │   ├── database.py
│   │   └── request.py
│   ├── setting.py
│   └── utils                       # Misc function and Constant
│       ├── constant.py
│       └── utility_function.py
├── .env                            # Environment variable being used (excluded from git)
├── .env.example                    # Example of environment variable
└── tests                           # Test Class location (integration & unit test)
    ├── routes
    │   └── test_test_route.py
    ├── services
    └── utils

10 directories, 15 files
```