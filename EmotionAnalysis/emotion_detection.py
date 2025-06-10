# emotion_detection.py
"""
This module defines emotion_detector(), which calls Watson NLP and returns a simple dict.
"""

import json
import requests

def emotion_detector(text_to_analyse):
    """
    Returns a dict with keys:
      - label:   emotion
      - score:   float or None
      - error:   None or a short message
    """
    print(f"Received text_to_analyse: {text_to_analyse!r}")

    # 1) Empty‐input check
    if not text_to_analyse or text_to_analyse.strip() == "":
        return {
            "label": "ERROR_No Text Provided",
            "score": None,
            "error": "No text provided. Input text"
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
    if response.status_code != 200:
        print(f"Error with status code: {response.status_code}")
        return {
            "label": None,
            "score": None,
            "error": f"Text is unparsable. Please provide meaningful text."
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
        return {"label": None, "score": None, "error": f"Unexpected response format: {e}"}

    return emotions