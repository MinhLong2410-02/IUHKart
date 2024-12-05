from transformers import pipeline
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

def analyze_sentiment(text):
    sentiment_pipeline = pipeline("text-classification", model="5CD-AI/Vietnamese-Sentiment-visobert", device=0)
    return sentiment_pipeline(text)#[0]['label']

if __name__ == "__main__":
    result = analyze_sentiment("Tôi rất vui vì được gặp bạn")
    print(result)
    # [{'label': 'POS', 'score': 0.9990874528884888}]