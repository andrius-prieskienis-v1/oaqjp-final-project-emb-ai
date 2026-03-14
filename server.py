"""Flask application for simple emotion detection.

This module exposes two HTTP endpoints:

- ``GET /emotionDetector`` — Accepts a query parameter ``textToAnalyze`` and
  returns a one-line summary of detected emotions and the dominant emotion.
- ``GET /`` — Renders the index page (``templates/index.html``).

The app depends on an external helper: ``EmotionDetection.emotion_detection.emotion_detector``,
which should return a mapping with at least these keys:
``anger, disgust, fear, joy, sadness, dominant_emotion``. If ``dominant_emotion`` is
``None``, the endpoint answers with a friendly validation message.

Run locally with:
    python app.py
and open http://127.0.0.1:5000/

Example request:
    GET /emotionDetector?textToAnalyze=I%20love%20this%20new%20technology.
Example response:
    For the given statement, the system response is 'anger': 0.01, 'disgust': 0.00,
    'fear': 0.00, 'joy': 0.97 and 'sadness': 0.05. The dominant emotion is joy.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")
@app.route("/emotionDetector")
def sent_analyzer():
    """Analyze emotions for the provided text and return a formatted summary.

    Expects a query parameter named ``textToAnalyze``. Delegates the analysis to
    ``emotion_detector`` and formats the returned scores into a human‑readable string.
    If the detector returns ``dominant_emotion`` as ``None``, a validation message is
    returned instead.

    Query Parameters:
        textToAnalyze (str): The input text to analyze. If missing or empty, the
            downstream detector may return an invalid result, which is handled by
            returning an informative message.

    Returns:
        str: A one‑line summary containing the five emotion scores (anger, disgust,
        fear, joy, sadness) and the detected dominant emotion, or a validation
        message if input is invalid.
    """

    text_to_analyze = request.args.get('textToAnalyze')
    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        result_text = "Invalid text! Please try again!"
    else:
        result_text = (
            "For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} "
            f"and 'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

    return result_text

@app.route("/")
def render_index_page():
    """Render the landing page.

    Returns:
        str: Rendered HTML for ``index.html`` from the app's templates directory.
    """

    return render_template('index.html')

if __name__ == "__main__":
    # Development entrypoint:
    #   - Accessible on all interfaces at port 5000.

    app.run(host="0.0.0.0", port=5000)
