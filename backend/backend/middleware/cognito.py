from django.http import JsonResponse
from django.conf import settings
from functools import wraps
import jwt
import time
import requests

class CognitoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 从请求头获取 JWT token
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            request.cognito_user = self.validate_token(token)
        else:
            request.cognito_user = None
            
        response = self.get_response(request)
        return response
    
    def validate_token(self, token):
        try:
            # 从 Cognito 获取公钥
            keys_url = f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
            response = requests.get(keys_url)
            keys = response.json()['keys']
            
            # 解码 token header 获取 kid
            headers = jwt.get_unverified_header(token)
            kid = headers['kid']
            
            # 查找匹配的公钥
            key = next((k for k in keys if k['kid'] == kid), None)
            if not key:
                return None
                
            # 验证 token
            decoded = jwt.decode(
                token,
                key,
                algorithms=['RS256'],
                audience=settings.COGNITO_CLIENT_ID
            )
            
            # 验证过期时间
            if decoded['exp'] < time.time():
                return None
                
            return decoded
            
        except Exception as e:
            print(f"Token validation error: {str(e)}")
            return None 