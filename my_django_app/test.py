from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
import torch

model_name = "ruanchaves/bert-base-portuguese-cased-assin2-similarity"
s1 = "ela pulou pra dentro do apartamento"
s2 = "ela pulou de volta pra dentro do mesmo prédio"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
config = AutoConfig.from_pretrained(model_name)
model_input = tokenizer(*([s1], [s2]), padding=True, return_tensors="pt")
with torch.no_grad():
    output = model(**model_input)
    score = output[0][0].detach().numpy().item()
    print(f"Similarity Score: {np.round(float(score), 4)}")
