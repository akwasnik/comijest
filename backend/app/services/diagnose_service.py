import os
import threading
import requests
import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from ..config import MODEL_DIR, MODEL_MAX_LENGTH, TRANSLATION_PROVIDER, LIBRE_TRANSLATE_URL


class DiagnoseService:
    _lock = threading.Lock()
    _loaded = False
    _tokenizer = None
    _model = None
    _label_encoder = None
    _device = None

    @classmethod
    def _load(cls):
        if cls._loaded:
            return
        with cls._lock:
            if cls._loaded:
                return

            if not MODEL_DIR or not os.path.isdir(MODEL_DIR):
                raise RuntimeError("MODEL_DIR is not set or does not exist")

            cls._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            cls._tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
            cls._model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
            cls._model.to(cls._device)
            cls._model.eval()

            label_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
            if not os.path.isfile(label_path):
                raise RuntimeError("label_encoder.pkl not found in MODEL_DIR")

            cls._label_encoder = joblib.load(label_path)
            cls._loaded = True

    @classmethod
    def _translate(cls, text, source, target):
        if TRANSLATION_PROVIDER != "libre":
            return text

        resp = requests.post(LIBRE_TRANSLATE_URL, json={
            "q": text,
            "source": source,
            "target": target,
            "format": "text"
        }, timeout=30)
        resp.raise_for_status()
        return resp.json()["translatedText"]

    @classmethod
    def diagnose(cls, text_pl, top_k=5):
        cls._load()

        # PL -> EN
        text_en = cls._translate(text_pl, "pl", "en")

        inputs = cls._tokenizer(
            text_en,
            return_tensors="pt",
            truncation=True,
            max_length=MODEL_MAX_LENGTH,
        )
        inputs = {k: v.to(cls._device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = cls._model(**inputs).logits

        probs = torch.softmax(logits, dim=-1)[0]
        k = min(int(top_k), probs.shape[0])
        top_probs, top_ids = torch.topk(probs, k=k)

        labels_en = cls._label_encoder.inverse_transform(top_ids.cpu().numpy())

        results = []
        for label_en, prob in zip(labels_en, top_probs.tolist()):
            label_pl = cls._translate(label_en, "en", "pl")
            results.append({
                "label_pl": label_pl,
                "prob": float(prob)
            })

        return {"top5": results}
