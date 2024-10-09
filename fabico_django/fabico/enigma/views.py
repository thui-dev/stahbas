from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect

##### Artificial Inteligence
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
import torch
###############

def Ai_Str_Cmp(input1, input2):
    s1 = input1
    s2 = input2
    model_name = "ruanchaves/bert-base-portuguese-cased-assin2-similarity"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = AutoConfig.from_pretrained(model_name)
    model_input = tokenizer(*([s1], [s2]), padding=True, return_tensors="pt")
    with torch.no_grad():
        output = model(**model_input)
        score = output[0][0].detach().numpy().item()
        return np.round(float(score), 4)

# STATES salvos em cada session, pois URLs não podem salvar vazar informação
LEVEL = 1
ENIGMA_FINALIZADO = False
"""
sexo(index 0) é a resposta da fase 1, e leva -> fase 2. bunda(index 1) é a resposta da fase 2, e leva -> fase 3
None é uma fase com resposta analisada por IA.

Desse jeito, qualquer resposta pode ser dada em qualquer Input,
porque eu vou checar se reposta in lista de respostas.
e tu vai pular pra fase seguinte à da resposta dada, como 'checkpoints'
"""
respostas = [None, None, "chimarrão", "final"]


def index(request):

    #resetar níveis sempre que entrar no index
    global LEVEL
    LEVEL = 1

    if request.method == "GET":
        return render(request, "enigma/index.html")
    else:
        return redirect("enigma")

def enigma(request):

    global ENIGMA_FINALIZADO, LEVEL

    if request.method == "GET":
         return render(request, f"enigma/enigma{LEVEL}.html")

    # em caso de POST

    if ENIGMA_FINALIZADO:
        #retorna confirmação que acabou, e registramos na DB a equipe
        equipe = request.POST.get("select")
        bunda = models.Answers(equipe=equipe, timestamp=datetime.now())
        bunda.save()
        return render(request, "enigma/final.html",{
            "message": equipe
        })

    #durante o enigma

    ##conferindo se resposta tá correta
    final_answer = request.POST["resposta"].lower()
    if final_answer in respostas:
        LEVEL = respostas.index(final_answer) + 2

    # CASOS ESPECIAIS
    ## final do enigma - útltima resposta
    if final_answer == "final":
        ENIGMA_FINALIZADO = True
        return render(request, "enigma/final.html")

    if LEVEL == 1:
        if final_answer == "fabico para sempre" or final_answer == "fabicoparasempre":
            LEVEL += 1

    if LEVEL == 2:
        this_answer = "ela pulou pra dentro do apartamento"
        if Ai_Str_Cmp(final_answer, this_answer) >= 3.8:
            LEVEL += 1
            return render(request, f"enigma/enigma{LEVEL-1}.html",{
                "message1": final_answer,
                "message2": this_answer
            })

    if LEVEL == 3:
        this_answer = "macacos não sobem pinheiros"
        if Ai_Str_Cmp(final_answer, this_answer) >= 3.3:
            LEVEL += 1
            return render(request, f"enigma/enigma{LEVEL-1}.html",{
                "message1":final_answer,
                "message2":this_answer
            })

    #enigma não acabou, e resposta errada - só atualiza a página
    return redirect("enigma")


