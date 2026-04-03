from typing import Annotated, Literal,Optional
from pydantic import BaseModel, computed_field,Field

class Patient(BaseModel):
    id:Annotated[str,Field(description='Id of patient',examples=['POO10'])]
    name:Annotated[str,Field(description='Name of patient')]
    city:Annotated[str,Field(description="name of city")]
    age:Annotated[int,Field(gt=0,lt=110,description='age of patient')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='gender of patient')]
    height: Annotated[float, Field(gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field( gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'




class Patient_Update(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

