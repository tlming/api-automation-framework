from pydantic import BaseModel
from typing import Optional

# ----- 地理坐标（全选填） -----
class Geo(BaseModel):
    lat: Optional[str] = None
    lng: Optional[str] = None

# ----- 地址（全选填） -----
class Address(BaseModel):
    street: Optional[str] = None
    suite: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    geo: Optional[Geo] = None   # 地址中的地理坐标也变为可选

# ----- 公司（全选填） -----
class Company(BaseModel):
    name: Optional[str] = None
    catchPhrase: Optional[str] = None
    bs: Optional[str] = None

# ----- 顶层用户（全选填） -----
class UserRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None          # 可用 EmailStr 但需额外安装
    address: Optional[Address] = None    # 地址整体可选
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[Company] = None    # 公司整体可选