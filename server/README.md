# Chatbot server

## Dependencies

Python version 3.10+. (Personally I am using 3.10.13.)

## To run locally

1. Initialize virtual env (one-time)
```sh
python -m venv .venv
```

2. Switch current python to `.venv`'s python
```sh
source .venv/bin/activate
```

3. Install the dependencies (one-time or if you face any dependency issues)
```sh
pip install -r requirements.txt
```

4. Run development server 
```sh
fastapi dev main.py
```
