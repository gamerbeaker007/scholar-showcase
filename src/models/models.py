from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum

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
    discord_enabled = Column(Boolean, nullable=False)
    email = Column(String, nullable=True)
    email_enabled = Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "account": self.account,
            "role": self.role.name if self.role else None,
            "discord_reference": self.discord_reference,
            "discord_enabled": self.discord_enabled,
            "email": self.email,
            "email_enabled": self.email_enabled,
        }
