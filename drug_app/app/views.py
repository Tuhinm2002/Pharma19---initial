from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import *
import pandas as pd
import os
import subprocess
from padelpy import from_smiles
import numpy as np
import pickle
from sklearn.feature_selection import VarianceThreshold

# Create your views here.

def model_fitting(file):
    X = pd.read_csv(file)
    X = X['canonical_smiles']
    X_np = np.asarray(X)
    a = []
    for i in X_np:
        a.append(i)
    from_smiles(a,output_csv='descripter.csv',fingerprints=True,descriptors=False)
    input_x = pd.read_csv('descripter.csv')
    input_x = input_x.drop(columns=['Name'],axis=1)
    model = pickle.load(open('trained_model.pkl','rb'))
    global res
    res = model.predict(input_x)
    os.remove('descripter.csv')
    

def home(request):
    if request.method == 'POST':
        file = request.FILES['file']
        document = File.objects.create(file = file)
        document.save()
        model_fitting(document.file)
        # return HttpResponse("Your File was saved")
    return render(request,'home.html')


def output(request):
    return render(request,"output.html",{"res":res})