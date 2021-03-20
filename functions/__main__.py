# coding: utf-8
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    # WatsonAssistantの初期設定
    authenticator = IAMAuthenticator('<your apikey>')
    assistant = AssistantV1(
        version='2020-04-01',
        authenticator = authenticator
    )
    assistant.set_service_url('https://gateway-tok.watsonplatform.net/assistant/api')

    # Firebase Realtime Databaseの初期設定
    if not firebase_admin._apps:
        cred = credentials.Certificate('<your service account json>')
        firebase_admin.initialize_app(cred, {
            'databaseURL': '<your databaseURL>',
        })

    search_text = dict["text"]

    # WatsonAssistantからユーザー入力への応答の取得
    response=assistant.message(
        workspace_id='<your workspace_id>',
        input={
            'text': search_text
        }
    ).get_result()
    command = response["output"]["text"][0]

    # Firebase Realtime Databaseのgeneralからデータの取得
    general_ref = db.reference('/general')
    commands = []
    options = []
    for k, v in general_ref.get()[command].items():
        if v["type"] == "cmd":
            commands.append({
                "label": k,
                "type": v["type"],
                "options": [],
                "description": v["description"]
            })
        elif v["type"] == "opt":
            options.append({
                "label": k,
                "type": v["type"],
                "description": v["description"]
            })
    for item in commands:
        item["optionsList"] = options

    result = {
        "commands": commands
    }

    return result