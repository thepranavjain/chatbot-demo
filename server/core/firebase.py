import os

from firebase_admin import credentials


service_account_path = os.path.join(
    os.path.dirname(__file__), "..", "serviceAccountKey.json"
)


firebase_cred = credentials.Certificate(service_account_path)
