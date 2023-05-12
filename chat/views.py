from django.shortcuts import render, redirect
from django.http import JsonResponse
import pickle
import pandas as pd
import random
# Create your views here.
rdf = pd.read_csv(r'E:\python\VizartGallery\chat\static\csv\bot_response_dataset.csv')

def load_model():
    with open(r'chat\static\models\model.pkl', 'rb') as f:
        return pickle.loads(f.read())

def index(request):
    
    
    return render(request, 'chat/index.html')


def predict_tag(txt='Hello world', vectorizer=None,
                model=None,binarizer=None,*args,**kwargs):
    input_vector = vectorizer.transform([txt])
    result = model.predict(input_vector)
    output_tag = binarizer.inverse_transform(result)
    return output_tag[0]

def get_bot_reply(predicted_tag):
    resultdf = rdf[rdf['tag']==predicted_tag] 
    responses = resultdf.response.to_list()
    return random.choice(responses)


def predict(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        model_data = load_model()
        tag = predict_tag(query, **model_data)
        if tag:
            response = get_bot_reply(tag)
        else:
            response = 'sorry, i am still learning. Call us to get more info'
    else:
        response = 'please ask me a question'

    return JsonResponse({'botreply':response, 'query' : query})