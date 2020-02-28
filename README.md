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
5. Run web services
   ```
    python app/main.py
   ```
