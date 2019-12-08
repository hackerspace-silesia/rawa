# rawa
project for gruba.it hackathon 2019 Dec

````
virtualenv venv3 -ppython3
source venv3/bin/activate
````

# install dev

```
# (in venv)
python setup.py develop
```

# how to run dev

```
# (in venv)
alembic upgrade head
FLASK_DEBUG=1 FLASK_APP=rawa/app.py python -m flask run
```
