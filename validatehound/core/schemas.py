# core/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

#USER SCHEMA FOR RUSTHOUND-CE
class Ace(BaseModel):
    InheritanceHash: str
    IsInherited: bool
    PrincipalSID: str
    PrincipalType: str
    RightName: str

class ContainedBy(BaseModel):
    ObjectIdentifier: str = Field(..., alias="ObjectIdentifier")
    ObjectType: str = Field(..., alias="ObjectType")

class Properties(BaseModel):
    name: str
    distinguishedname: Optional[str] = None
    domain: Optional[str] = None

class User(BaseModel):
    ObjectId: str = Field(..., alias="ObjectIdentifier")
    Properties: Properties
    Aces: Optional[List[Ace]] = []
    AllowedToDelegate: Optional[List[str]] = []
    ContainedBy: Optional[ContainedBy]
    DomainSID: Optional[str] = None
    HasSIDHistory: Optional[List[str]] = []
    IsACLProtected: Optional[bool] = False
    IsDeleted: Optional[bool] = False
    PrimaryGroupSID: Optional[str] = None
    SPNTargets: Optional[List[str]] = []
    UnconstrainedDelegation: Optional[bool] = False

    @field_validator("ContainedBy", mode="before")
    def parse_containedby(cls, v):
        if isinstance(v, dict):
            return ContainedBy(**v)
        return v

# GROUP SCHEMA RUSTHOUND-CE

class GroupProperties(BaseModel):
    name: str
    distinguishedname: Optional[str] = None
    domain: Optional[str] = None
    domainsid: Optional[str] = None
    isaclprotected: Optional[bool] = False
    highvalue: Optional[bool] = False
    samaccountname: Optional[str] = None
    description: Optional[str] = None
    whencreated: Optional[int] = None
    admincount: Optional[bool] = False

class GroupMember(BaseModel):
    ObjectIdentifier: str
    ObjectType: str

class Group(BaseModel):
    ObjectId: str = Field(..., alias="ObjectIdentifier")
    Properties: GroupProperties
    Members: Optional[List[GroupMember]] = []
    Aces: Optional[List[Ace]] = []
    ContainedBy: Optional[ContainedBy]
    IsDeleted: Optional[bool] = False
    IsACLProtected: Optional[bool] = False

    @field_validator("ContainedBy", mode="before")
    def parse_containedby(cls, v):
        if isinstance(v, dict):
            return ContainedBy(**v)
        return v

# === Schema registry ===
SCHEMA_MAP = {
    #"aiacas.json": Aiacas,  
    #"certtemplates.json": CertTemplate,  
    #"computers.json": Computer, 
    #"containers.json": Container,  
    #"domains.json": Domain,  
    #"enterprisecas.json": EnterpriseCA,  
    #"gpos.json": GPO,  
    "groups.json": Group, 
    #"issuancepolicies.json": IssuancePolicy,  
    #"ntauthstores.json": NTAuthStore,  
    #"ous.json": OU,  
    #"rootcas.json": RootCA, 
    #"sessions.json": Session, 
    "users.json": User,
}
