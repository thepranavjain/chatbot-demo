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

4. Env vars -

Make sure you populate a `.env` with required env vars. You may refer `sample.env.txt` for spec.

Also, have a `serviceAccountKey.json` from firebase in this dir for auth.

5. Run development server 
```sh
fastapi dev main.py
```

## Test

Install the dependencies (one-time or if you face any dependency issues)
```sh
pip install -r requirements.txt
```

Then run -
```sh
pytest
```
