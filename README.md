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
    python3 -m venv env
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
6. Run web service on dev environment
   ```
    uvicorn app.main:app --reload
   ```
7. Swagger can be accesed on [http://localhost:8000/docs](http://localhost:8000/docs).

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