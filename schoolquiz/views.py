from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from schoolquiz.models import quiz
from schoolquiz.forms import quizform
import time
def home(request):
    return render(request, "home.html")
def signup(request):
    form=UserCreationForm()
    if(request.method=='POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return home(request)
    return render(request,"signup.html")
def userlogin(request):
    if (request.method == 'POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            global count,score
            start_time = time.time()
            request.session['start_time'] = start_time
            count=0
            score=0
            request.session['score'] = score

            return quizz(request)
        else:
            return HttpResponse("Invalid login details")
    return render(request,'login.html')
def userlogout(request):
    logout(request)
    return userlogin(request)
def quizz(request):
    global count
    k = quiz.objects.order_by('?')[0]
    request.session['k']=k.answer
    count = count+1
    c=count
    if (count==11):
        score =request.session['score']
        n=int(request.session['score'])
        if(n>=5):
            start_time=request.session['start_time']
            elapsed_time = time.time() - start_time
            result="passed"
            return render(request, "quiz.html", {'count':count,'score':score,'result':result,'elapsed_time':elapsed_time})
        if (n <5):
            start_time = request.session['start_time']
            elapsed_time = round((time.time() - start_time),2)
            result = "failed"
            return render(request, "quiz.html", {'count': count, 'score': score, 'result': result,'elapsed_time':elapsed_time})
    else:
        return render(request, "quiz.html", {'k': k,'c':c})
def quizzcheck(request):
    global score

    if(request.method=="POST"):
        v = request.POST.get('options')
        a=request.session['k']
        if(v==a):
            f=1
            score=score +1
            request.session['score']=score
            return render(request, "quiz.html", {'f':f})
        if(v!=a):
            e=1
            return render(request, "quiz.html", {'e': e,'a':a})


    return quizz(request)



