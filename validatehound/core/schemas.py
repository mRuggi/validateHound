# core/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field


# === Base node models (semplificati) ===
class User(BaseModel):
    ObjectId: str = Field(..., alias="objectid")
    Name: str
    Domain: Optional[str] = None
    DistinguishedName: Optional[str] = None


class Group(BaseModel):
    ObjectId: str = Field(..., alias="objectid")
    Name: str
    Members: Optional[List[str]] = None


class Computer(BaseModel):
    ObjectId: str = Field(..., alias="objectid")
    Name: str
    Domain: Optional[str] = None
    OperatingSystem: Optional[str] = None


class Session(BaseModel):
    UserId: str
    ComputerId: str


# === Schema registry ===
SCHEMA_MAP = {
    "users.json": User,
    "groups.json": Group,
    "computers.json": Computer,
    "sessions.json": Session,
}
