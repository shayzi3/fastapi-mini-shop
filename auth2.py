import time

import jwt
import bcrypt
from fastapi import HTTPException

from config import Secrets 


class Auth:
    
    @staticmethod
    async def get_hashed_password(plain_text_password: str):
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


    @staticmethod
    async def check_password_hash(plain_text_password: str, hashed_password):
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    
    @staticmethod
    def encode_token(username):
        payload = {
            'scope': 'access_token',
            'sub' : username,
            "expires": time.time() + 3600
        }
        return jwt.encode(
            payload, 
            Secrets.SECRET,
            algorithm='HS256'
        )


    @staticmethod
    def decode_token(token) -> dict:
        try:
            payload = jwt.decode(token, Secrets.SECRET, algorithms=['HS256'])
            
            if payload['scope'] != 'access_token':
                raise HTTPException(status_code=15, detail='Scope for token invalid!')
            
            
            if payload['expires'] < time.time():
                raise HTTPException(status_code=101, detail='Token expired')
            
            return payload 
            
        
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=365, detail='Invalid token')


    @staticmethod
    def encode_refresh_token(username):
        payload = {
            'expires' : time.time() + 18000,
            'scope': 'refresh_token',
            'sub' : username
        }
        return jwt.encode(
            payload, 
            Secrets.SECRET,
            algorithm='HS256'
        )
        
        
    @classmethod
    def refresh_token(cls, refresh_token):
        try:
            payload = jwt.decode(refresh_token, Secrets.SECRET, algorithms=['HS256'])
            
            if payload['scope'] != 'refresh_token':
                raise HTTPException(status_code=16, detail='Scope for token invalid!')
            
            if payload['expires'] < time.time():
                raise HTTPException(status_code=102, detail='Token expired')
            
            new_token = cls.encode_token(payload['sub'])
            return new_token
        
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')
        
        
auth = Auth()