# rawa
project for gruba.it hackathon 2019 Dec

# install dev

```
# (in venv)
python setup.py develop
```

# dev

```
# (in venv)
alembic upgrade head
FLASK_DEBUG=1 FLASK_APP=rawa/app.py python -m flask run
```

