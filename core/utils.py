from rest_framework_simplejwt import refresh_token

def create_token(user):
    refresh = refresh_token.RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }