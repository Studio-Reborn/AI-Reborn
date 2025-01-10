'''
File Name : helpers
Description : 리사이클링 제품 추천 관련
Author : 이유민

History
Date        Author      Status      Description
2024.10.30  이유민      Created     
2024.10.30  이유민      Modified    리사이클링 제품 추천 기능 작성
2025.01.10  이유민      Modified    DB 연동
2025.01.10  이유민      Modified    DB에서 데이터 조회 후 리사이클링 제품 추천
'''
import json
from dotenv import load_dotenv
import os
import openai
from flask import jsonify
import pymysql


load_dotenv()
openai.api_key  = os.getenv('OPENAI_API_KEY')

# DB에서 리본 리메이크 제품 가져오기
def get_product_list():
    connection = pymysql.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USERNAME'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_DATABASE'),
        charset = "utf8mb4"
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM remake_product") 
            products = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    finally:
        connection.close()
    return products

def recommend(user_input: str) -> str:
    # 리본 리메이크 제품 리스트
    product_list = get_product_list()
    product_options = ""

    for i in range (0, len(product_list)):
        product_options += product_list[i]["name"]
    
        if i != len(product_list) - 1:
            product_options += ', '

    # 시스템 프롬프트 설정
    qa_system_prompt = f"""당신은 사용자의 요청과 가장 어울리는 리사이클링 주제를 추천하는 역할을 합니다.
    사용자가 입력한 내용에 기반하여 관련성 있는 리사이클링 주제를 추천해 주세요.
    리사이클링 주제는 {product_options} 중 하나로 정해야 하며, 사용자가 입력한 내용과 관련이 있어야 합니다.
    리사이클링 주제와 함께 추천하는 이유를 설명할 수 있어야 합니다.s
    결과는 JSON 형태로 다음과 같은 형태를 따라야 합니다:
    {{
        "theme": "리사이클링 주제",
        "reason": "추천하는 이유"
    }}
    입력된 내용: {{input}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": qa_system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7  
    )
    recommendation = json.loads(response.choices[0].message['content'].strip())

    # theme 기반 id 찾고 결과에 포함하기
    recommended_theme = recommendation["theme"]
    theme_id = next((product["id"] for product in product_list if product["name"] == recommended_theme), None)
    recommendation["id"] = theme_id

    return recommendation