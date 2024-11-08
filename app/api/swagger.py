'''
File Name : swagger
Description : api 및 swagger 관련
Author : 이유민

History
Date        Author      Status      Description
2024.10.30  이유민      Created     
2024.10.30  이유민      Modified    swagger 기본 코드 작성
2024.10.30  이유민      Modified    리사이클링 제품 추천 기능 추가
'''
from flask_restx import Api
from .recommend import recommend_api

api = Api(
    version='1.0',
    title='Reborn - AI',
    description='Reborn-AI API 문서',
    doc="/api-docs"
)

api.add_namespace(recommend_api, path='/recommend')