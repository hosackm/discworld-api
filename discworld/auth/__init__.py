import json
from flask import request, abort, current_app
from functools import wraps
from jose import jwt
from jose.exceptions import JWTError
from urllib.request import urlopen


def get_token_auth_header():
    auth = request.headers.get("Authorization")
    if not auth:
        abort(401)

    if "Bearer " not in auth:
        abort(401)

    return auth.split("Bearer ")[-1]


def check_permissions(permission, payload):
    if "permissions" not in payload:
        abort(403)

    if permission not in payload["permissions"]:
        abort(403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{current_app.config['AUTH0_DOMAIN']}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        abort(401)

    if "kid" not in unverified_header:
        abort(401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=current_app.config["AUTH0_AUDIENCE"],
                issuer=f"https://{current_app.config['AUTH0_DOMAIN']}/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            abort(401)
        except jwt.JWTClaimsError:
            abort(401)
        except Exception:
            abort(400)
    else:
        abort(400)


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_app.config.get("TESTING", False):
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            else:
                print("testing is enabled.  Bypassing authorization")
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
