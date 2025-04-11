import enum

from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class RoleEnum(str, enum.Enum):
    Undefined = "Undefined"
    Scholar = "Scholar"
    Manager = "Manager"


class User(Base):
    __tablename__ = 'users'

    account = Column(String, primary_key=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.Undefined)
    discord_reference = Column(String, nullable=True)
    email = Column(String, nullable=True)

    def to_dict(self):
        return {
            "account": self.account,
            "role": self.role.name if self.role else None,
            "discord_reference": self.discord_reference,
            "email": self.email,
        }
