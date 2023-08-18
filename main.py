from fastapi import FastAPI, HTTPException
from table import Secret_creation, Secret_reveal
import secrets
from typing import Dict
from datetime import datetime, timedelta
import uvicorn

test_case_app = FastAPI()

secrets_db = {}  # instead of normal DB

@test_case_app.post('/generate')
async def generate_secret(secret_data: Secret_creation) -> Dict[str, str]:
    secret_key = secrets.token_urlsafe(12)
    current_time = datetime.now().replace(microsecond=0)
    expiration_time = current_time + timedelta(minutes=10) # secret will expired after 10 min
    secrets_db[secret_key] = {
        'secret': secret_data.secret,
        'passphrase': secret_data.pass_phrase,
        'expiration_time': expiration_time
    }
    
    return {'secret_key': secret_key}
    

@test_case_app.post('/secrets/{secret_key}')
async def reveal_secret(secret_key: str, secret_data: Secret_reveal) -> Dict[str, str]:
    current_time = datetime.now().replace(microsecond=0)
    if secret_key in secrets_db:
        secret_info = secrets_db.get(secret_key)
        if secret_info['passphrase'] == secret_data.pass_phrase:
            expiration_time = secret_info['expiration_time']
            if current_time <= expiration_time:
                secret = secrets_db.pop(secret_key)
                return {'secret': secret['secret']}
            else:
                raise HTTPException(status_code=403, detail='Secret has expired')
        else:
            raise HTTPException(status_code=403, detail="Invalid passphrase")
    else:
        raise HTTPException(status_code=403, detail='Invalid secret key')


if __name__ == "__main__":
    uvicorn.run(test_case_app, host="0.0.0.0", port=80)