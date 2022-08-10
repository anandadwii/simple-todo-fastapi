# simple ToDo FASTAPI and mongoDB


ToDo API built using Fast Api python and mongoDB as database with role management.
user can create and fetch todo but cant update and delete. admin can crud user note and user account.
super admin can do anything in Swagger UI. literally anything.

technology used in this work:
- FAST API 
- pydantic 
- mongoDB with pymongo
- JWT Token

## How To Install 
- install mongo or mongodb compass and make sure port `27017` is not used
- clone this repo using git bash `git clone  https://github.com/anandadwii/simple-todo-fastapi.git` 
- run `pip install -r requirements.txt` to install all module needed

## How To Run
just run via main and dont forget to run mongodb with `27017` port.
after uvicorn run, go to browser and type `localhost:8000` and your will be redirected to Swagger UI.
if you want to use redoc, just use `localhost:8000/redoc`.





