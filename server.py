# server.py
"""
Simple server to run Watson AI to analyse emotions.
Receives:
    - input text string from html element
Returns:
    - dictionary with emotion scores and dominant emotion
    - throws error if input is blank
"""

from flask import Flask, render_template, request
from EmotionAnalysis.emotion_detection import emotion_detector

app = Flask("Sentiment Analyzer")

@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Route to emotion analyzer
    Receives:
        - Input string
    Returns:
        - Dictionary with emotions
        - Error if input is empty
    """
    text_to_analyze = request.args.get("textToAnalyze")

    # if no text, throw error
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!", 400

    # call function
    response = emotion_detector(text_to_analyze)

    # if response is None throw error
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!", 400

    response_text = f"For the given statement, the system response is \
    'anger': {response['anger']}, \
    'disgust': {response['disgust']}, \
    'fear': {response['fear']}, \
    'joy': {response['joy']} and \
    'sadness': {response['sadness']}. \
    The dominant emotion is {response['dominant_emotion']}."

    print(f"Returning response: {response_text}")
    return response_text

@app.route("/")
def render_index_page():
    """
    Default homepage
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
