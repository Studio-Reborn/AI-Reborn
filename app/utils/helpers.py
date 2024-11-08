'''
File Name : helpers
Description : 리사이클링 제품 추천 관련
Author : 이유민

History
Date        Author      Status      Description
2024.10.30  이유민      Created     
2024.10.30  이유민      Modified    리사이클링 제품 추천 기능 작성
'''
import json
from dotenv import load_dotenv
import os
import openai
from flask import jsonify

load_dotenv()
openai.api_key  = os.getenv('OPENAI_API_KEY')

def recommend(user_input: str) -> str:
    # 시스템 프롬프트 설정
    qa_system_prompt = """당신은 사용자의 요청과 가장 어울리는 리사이클링 주제를 추천하는 역할을 합니다.
    사용자가 입력한 내용에 기반하여 관련성 있는 리사이클링 주제를 추천해 주세요.
    리사이클링 주제는 지갑, 코스터, 에코백, 화분, 연필꽂이, 책갈피, 치약짜개 중 하나로 정해야 하며, 사용자가 입력한 내용과 관련이 있어야 합니다.
    리사이클링 주제와 함께 추천하는 이유를 설명할 수 있어야 합니다.s
    결과는 JSON 형태로 다음과 같은 형태를 따라야 합니다:
    {
        "theme": "리사이클링 주제",
        "reason": "추천하는 이유"
    }

    입력된 내용: {input}
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

    return recommendation