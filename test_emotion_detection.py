import unittest
from EmotionAnalysis.emotion_detection import emotion_detector

class TestEmotionAnalysis(unittest.TestCase):
    def test_emotion_detector(self):
        statements = {
            'I am glad this happened': 'joy',
            'I am really mad about this': 'anger',
            'I feel disgusted just hearing about this': 'disgust',
            'I am so sad about this': 'sadness',
            'I am really afraid that this will happen': 'fear'
        }

        for statement, emotion in statements.items():
            test = emotion_detector(statement)
            result = test['dominant_emotion']
            self.assertEqual(result, emotion)
            print(f"Done test for {result}")

if __name__=="__main__":
    unittest.main()