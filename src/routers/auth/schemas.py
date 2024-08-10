

from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


typeNAME = Annotated[str, Field(max_length=15, min_length=3)]
typePASS = Annotated[str, Field(max_length=20, min_length=8)]
typeEMAIL = Annotated[EmailStr, Field(min_length=12)]



class Reg(BaseModel):
     name: typeNAME
     password: typePASS 
     email: typeEMAIL
     


class Auth(BaseModel):
     name: typeNAME
     password: typePASS
     