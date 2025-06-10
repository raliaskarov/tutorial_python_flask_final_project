# emotion_detection.py
"""
This module defines emotion_detector(), which calls Watson NLP and returns a simple dict.
"""

import json
import requests

def emotion_detector(text_to_analyse):
    """
    Returns dict, for example:
      {'anger': 0.0043339236,
       'disgust': 0.00037549555, 
       'fear': 0.0034732423,
       'joy': 0.9947189,
       'sadness': 0.012704818,
       'dominant_emotion': 'joy'}
    """
    print(f"Received text_to_analyse: {text_to_analyse!r}")

    # 1) Empty‐input check
    if not text_to_analyse or text_to_analyse.strip() == "":
        return {
        'anger': None,
        'disgust': None, 
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
        }

    # 2) URL 
    url = ('https://sn-watson-emotion.labs.skills.network/v1'
        '/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    myobj = {"raw_document": {"text": text_to_analyse}}
    header = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
        }

    # 3) Call Watson and bail on non‐200
    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
    except requests.RequestException as e:
        print(f"Network/timeout error: {e}")
        return {"label": None, "score": None, "error": f"Request failed: {e}"}

    print("Response status code: ", response.status_code)
    if response.status_code == 400:
        print(f"Error with status code: {response.status_code}")
        emotions = {
            'anger': None,
            'disgust': None, 
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    if response.status_code != 400:
    print(f"Error with status code: {response.status_code}")
    emotions = {
        'anger': None,
        'disgust': None, 
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }


    # 4) Parse JSON and return
    try:
        data = response.json()

        emotions = data['emotionPredictions'][0]['emotion']
        dominant = max(emotions, key = emotions.get)
        emotions['dominant_emotion'] = dominant

        # save to json
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    return emotions