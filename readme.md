# Mini Insta

## How to run the app

1. Clone the repo
```bash
>$ git clone {repo_url.git}
```
2. Setup virtual environment
```bash
> /mini_insta$ python3 venv -m env
> /mini_insta$ source env/bin/activate # for Windows -> env\Scripts\activate.bat 
```

3. Download requirements
```bash
> (env) /mini_insta$ pip3 install -r requirements.txt
```

4. Setup environment varaibles
```bash
> (env) /mini_insta$ touch .env
> (env) /mini_insta$ echo "SECRET_KEY={any random hash}" >> .env
```

5. Migrate and start the server
```bash
> (env) /mini_insta$ python3 manage.py migrate
> (env) /mini_insta$ python3 manage.py runserver
```