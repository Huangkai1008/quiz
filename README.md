# Quiz

Quiz is a Online q&a platform with Flask.

在线问答平台

## Installation

Make sure you have installed [pipenv](https://docs.pipenv.org/en/latest/)

```bash
pip install pipenv
```

Then install libs

```bash
pipenv install
```

## Usage

```bash
flask run
celery -A celery_worker.celery worker -l info -P gevent   # Start the celery worker
celery -A celery_worker.celery beat -l info               # Start the celery beat
flower -A celery_worker.celery  -l info                   # Start the flower
```

## License
[MIT](https://www.mit-license.org/)
