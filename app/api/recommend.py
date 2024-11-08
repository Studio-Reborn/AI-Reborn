'''
File Name : recommend
Description : 리사이클링 제품 추천 관련
Author : 이유민

History
Date        Author      Status      Description
2024.10.30  이유민      Created     
2024.10.30  이유민      Modified    리사이클링 제품 추천 기능 작성
'''
from flask import request
from flask_restx import Namespace, Resource, fields
from app.utils.helpers import recommend

recommend_api = Namespace('Recommend', description='리사이클링 제품 추천')

@recommend_api.route('')
class Recommender(Resource):
    @recommend_api.response(200, '제품 추천 성공', recommend_api.model('Response', {
        'theme': fields.String(description='추천 주제'),
        'reason': fields.String(description='추천 이유')
    }))
    @recommend_api.response(400, '잘못된 요청', recommend_api.model('ErrorResponse', {
        'error': fields.String(description='잘못된 요청입니다.')
    }))
    @recommend_api.response(401, '인증 실패', recommend_api.model('ErrorResponse', {
        'error': fields.String(description='인증에 실패했습니다.')
    }))
    @recommend_api.response(500, '서버 오류', recommend_api.model('ErrorResponse', {
        'error': fields.String(description='서버에 오류가 발생했습니다.')
    }))
    def get(self):
        thing = request.args.get('thing')

        if not thing:
            return {"error": "잘못된 요청입니다. 'thing' 파라미터가 필요합니다."}, 400

        recommendation = recommend(thing)

        return recommendation, 200