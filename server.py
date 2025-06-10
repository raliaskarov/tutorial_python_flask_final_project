# server.py

from flask import Flask, render_template, request
from EmotionAnalysis.emotion_detection import emotion_detector

app = Flask("Sentiment Analyzer")

@app.route("/emotionDetector")
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze")

    # if no text, throw error
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "String empty, please provide text", 400

    # call function
    response = emotion_detector(text_to_analyze)

    # if error in response, throw it
    if response.get("error"):
        return f"Error: {response['error']}", 400

    response_text = f"For the given statement, the system response is \
    'anger': {response['anger']}, \
    'disgust': {response['disgust']}, \
    'fear': {response['fear']}, \
    'joy': {response['joy']} and \
    'sadness': {response['sadness']}. \
    The dominant emotion is {response['dominant_emotion']}."

    return response_text

@app.route("/")
def render_index_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    
