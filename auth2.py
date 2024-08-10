import time

import jwt
from fastapi import HTTPException
# from passlib.context import CryptContext # used for hashing the password

from config import Secrets 


class Auth:
    # hasher = CryptContext(schemes=['bcrypt'])

    # def encode_password(self, password):
    #     return self.hasher.hash(password)

    # def verify_password(self, password, encoded_password):
    #     return self.hasher.verify(password, encoded_password)


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
    def decode_token(token) -> str:
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