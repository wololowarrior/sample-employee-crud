import re
import uuid
from dataclasses import dataclass, field
from enum import  Enum
from typing import  Optional

class Departments(Enum):
    Technology = 1
    Marketing = 2
    Sales = 3
    HR = 4
    Business = 5
    Management = 6



@dataclass
class Employee:
    name: str
    email: Optional[str]
    phone: int
    department : str
    country: str
    dept_id: Optional[int] = None
    country_id: Optional[int] = None
    ID: str = uuid.uuid4()

    def __post_init__(self):
        regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if self.email and not re.match(regex_email, self.email):
            raise ValueError("It's not an email address.")
        regex_phone = "[1-9][0-9]{9}"
        if not self.phone:
            raise ValueError("phone number not provided")
        elif not re.match(regex_phone, str(self.phone)):
            raise ValueError("phone cannot exceed 10 int.")

        if not hasattr(Departments, self.department):
            raise ValueError("Please check department name")

    def to_json(self):
        return dict(name=self.name, id=self.ID, email=self.email, phone=self.phone, country=self.country, department=self.department)
