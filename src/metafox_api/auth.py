import os

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

from metafox_shared.models.user import User
from metafox_shared.constants.string_constants import *

load_dotenv()

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL", ""),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID", ""),
    realm_name=os.getenv("KEYCLOAK_REALM_NAME", ""),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET", ""),
    verify=True
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=os.getenv("KEYCLOAK_AUTHORIZATION_URL", ""),
    tokenUrl=os.getenv("KEYCLORAK_TOKEN_URL", ""),
    refreshUrl=os.getenv("KEYCLOAK_REFRESH_URL", "")
)

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )
    
# Get the payload/token from keycloak
async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Get user infos from the payload
async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    try:
        return User(
            id=payload.get(SUB),
            username=payload.get(PREFERED_USERNAME),
            email=payload.get(EMAIL),
            first_name=payload.get(GIVEN_NAME),
            last_name=payload.get(FAMILY_NAME),
            realm_roles=payload.get(REALM_ACCESS, {}).get(ROLES, []),
            client_roles=payload.get(REALM_ACCESS, {}).get(ROLES, [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )