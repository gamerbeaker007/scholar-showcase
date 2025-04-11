from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
import enum

Base = declarative_base()


class RoleEnum(str, enum.Enum):
    Undefined = "Undefined"
    Scholar = "Scholar"
    Manager = "Manager"


class PreferredModesEnum(str, enum.Enum):
    Any = "Any"
    Wild = "Wild"
    Modern = "Modern"
    WildModern = "Wild&Modern"
    Survival = "Survival"


class RewardSplitEnum(str, enum.Enum):
    Debatable = "Debatable"
    SPS_0_100 = "0/100 SPS"
    SPS_25_75 = "25/75 SPS"
    SPS_50_50 = "50/50 SPS"
    SPS_75_25 = "75/27 SPS"
    SPS_100_0 = "100/0 SPS"


class User(Base):
    __tablename__ = 'users'

    account = Column(String, primary_key=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.Undefined)
    discord_reference = Column(String, nullable=True)
    preferred_mode: Mapped[PreferredModesEnum] = mapped_column(Enum(PreferredModesEnum), nullable=True)
    reward_split: Mapped[RewardSplitEnum] = mapped_column(Enum(RewardSplitEnum), nullable=True)

    def to_dict(self):
        user_dict = {
            "account": self.account,
            "role": self.role.name if self.role else None,
            "discord_reference": self.discord_reference,
            "preferred_mode": self.preferred_mode.value if self.preferred_mode else None,
            "reward_split": self.reward_split.value if self.reward_split else None,
        }
        return user_dict
