import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from core.models import User

@database_sync_to_async
def get_user(token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get('user_id')
        
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return AnonymousUser()
        return user

    except (DecodeError, ExpiredSignatureError, InvalidTokenError) as e:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            query_string = scope['query_string'].decode()
            token = None
            for param in query_string.split('&'):
                key, value = param.split('=')
                if key == 'token':
                    token = value
                    break
        except (ValueError, IndexError):
            token = None
        scope['user'] = await get_user(token)
        return await super().__call__(scope, receive, send)