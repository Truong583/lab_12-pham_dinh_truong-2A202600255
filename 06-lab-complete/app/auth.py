"""
Auth Module — Nâng cấp hỗ trợ cả API Key và JWT Token.
Chuẩn bảo mật đa lớp cho Production.
"""
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# Header cho API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
# Header cho Bearer Token (JWT)
security_bearer = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Tạo JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    """Xác thực JWT Token"""
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_api_key(api_key: str = Security(api_key_header)):
    """Xác thực API Key"""
    if api_key == settings.agent_api_key:
        return "admin"
    return None

def get_current_user(
    api_key: str = Depends(verify_api_key),
    user_id: str = Depends(verify_token)
) -> str:
    """
    Dependency kết hợp: Chấp nhận cả API Key hoặc JWT Token.
    """
    user = api_key or user_id
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required: X-API-Key header or Bearer Token"
        )
    return user
