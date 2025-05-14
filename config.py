import os
import secrets
from dotenv import load_dotenv

# Create .env with SECRET_KEY if it doesn't exist
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        secret_key = secrets.token_hex(32)
        f.write(f'SECRET_KEY={secret_key}\n')

# Load variables from .env into environment
load_dotenv()

# Access SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    # Edge case: .env exists but SECRET_KEY is missing
    secret_key = secrets.token_hex(32)
    with open('.env', 'a') as f:
        f.write(f'SECRET_KEY={secret_key}\n')
    SECRET_KEY = secret_key
