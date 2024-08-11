import datetime
import time

import jwt
import bcrypt
from fastapi import HTTPException, Response

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
                raise HTTPException(status_code=245, detail='Scope for token invalid!')
                
            return payload 
        
        except jwt.InvalidTokenError:
            return {'error': 305}


    @staticmethod
    def encode_refresh_token(username):
        payload = {
            'scope': 'refresh_token',
            'sub' : username,
            "expires": time.time() + 18000
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
                raise HTTPException(status_code=246, detail='Scope for token invalid!')
            
            new_token = cls.encode_token(payload['sub'])
            return new_token
        
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')
        
        
    @classmethod
    async def get_access_refresh_tokens(cls, username: str, response: Response):
        token_access = cls.encode_token(username)
        response.set_cookie(
            key='access_token', 
            value=token_access,
            httponly=True,
            expires=3600
        )
        
        token_refresh = cls.encode_refresh_token(username)
        response.set_cookie(
            key='refresh_token',
            value=token_refresh,
            httponly=True,
            expires=18000
        )
        return {'status': 101, 'access_token': token_access, 'refresh_token': token_refresh}
    
    
    @classmethod
    async def check_refresh_and_access_tokens(
        cls, 
        access_token, 
        refresh_token_, 
        response: Response
    ) -> dict:
        new_token = cls.refresh_token(refresh_token_)
        decode = cls.decode_token(access_token)
     
        # Access token expired
        if 'error' in decode.keys():
            response.set_cookie(
                key='access_token',
                value=new_token,
                httponly=True
            )
            return cls.decode_token(new_token)
        return decode
        
        
auth = Auth()