

from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


typeNAME = Annotated[str, Field(max_length=15, min_length=3)]
typePASS = Annotated[str, Field(max_length=20, min_length=8)]



class Reg(BaseModel):
     name: typeNAME
     password: typePASS 
     email: EmailStr
     


class Auth(BaseModel):
     name: typeNAME
     password: typePASS
     