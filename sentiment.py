from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
vader = SentimentIntensityAnalyzer()
HF_MODEL = 'cardiffnlp/twitter-roberta-base-sentiment'
_nlp = None
def init_hf():
    global _nlp
    if _nlp is None:
        tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL)
        _nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
def score_text(text, use_hf=False):
    if use_hf:
        try:
            if _nlp is None:
                init_hf()
            res = _nlp(text[:512])
            lab = res[0]['label']
            sc = float(res[0]['score'])
            return lab, sc
        except Exception:
            pass
    vs = vader.polarity_scores(text)
    comp = vs['compound']
    if comp >= 0.05:
        return 'POSITIVE', comp
    elif comp <= -0.05:
        return 'NEGATIVE', comp
    else:
        return 'NEUTRAL', comp
