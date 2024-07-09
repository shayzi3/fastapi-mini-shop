

from typing import Annotated
from pydantic import BaseModel, Field


typeNAME = Annotated[str, Field(max_length=15, min_length=3)]
typePASS = Annotated[str, Field(max_length=20, min_length=8)]



class Registration(BaseModel):
     name: typeNAME
     password: typePASS     
     


class ChangeName(BaseModel):
     name: typeNAME
     password: typePASS
     new_name: typeNAME
     
     
     
class ChangePassword(BaseModel):
     password: typePASS
     new_password: typePASS