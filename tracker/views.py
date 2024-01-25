from django.db.models import Q

from django.shortcuts import render,redirect,reverse

from django.shortcuts import get_object_or_404

from django.http import HttpResponse,HttpResponseRedirect

from .forms import ItemModelForm

from . models import Item

from django.db.models import Sum

from django.contrib.auth import authenticate,login

from .forms import SignUpForm

import re,json

import requests

def signup(request):                       #View for signing up using custom inbuilt UserCreationForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():                #Checking for form validation and retriving username,pass from POST data
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)            #User is logged in
            return HttpResponseRedirect('/item')
    else:
        form = SignUpForm()                 # IF not logged in then Show empty form
    return render(request, 'registration/signup.html', {'form': form})

def add_item(request):                      # Add all expenses items
    k=Item.objects.aggregate(Sum('price'))   # gets total sum of expenses
    l=json.dumps(k)                          # converts into json string
    p=re.findall("\d+",l)                    #Retrives numerical part from returned string
    item = Item.objects.all()
    if request.method == "POST":
        form = ItemModelForm(request.POST,request.FILES)  #request.FILES contains uploaded files
        if form.is_valid():
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.save()
            form = ItemModelForm()
            return HttpResponseRedirect('/item') #redirects to same page after POST
    else:
        form = ItemModelForm()
    return render(request, "tracker/index.html", {'form': form ,'item':item,'sum':p })


def update(request,id):                       # Editing submitted data
    instance=get_object_or_404(Item,id=id)
    form=ItemModelForm(data=request.POST, files=request.FILES, instance=instance) #posted files will be in request.FILES
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
    context={
        "name":instance.name,
        "price":instance.price,
        "instance":instance,
        "form":form,
    }
    return render(request,"tracker/update.html",context)


def display(request):                                     #displaying all items
    k = Item.objects.aggregate(Sum('price'))
    l = json.dumps(k)
    p = re.findall("\d+", l)
    item = Item.objects.all()
    return render(request,"tracker/table.html",{'items':item ,'sum':p})


def delete(request,id):                                    #deleting items by primary key on click
    deleteitem=get_object_or_404(Item,pk=id).delete()
    return HttpResponseRedirect('/display')

def sortbyname(request):                                   # sorting by name
    sname=Item.objects.order_by('name').all()
    return render(request,"tracker/sname.html",{'name':sname})


def sortbyprice(request):                                  #sorting by price
    sprice=Item.objects.order_by('price').all()
    return render(request,"tracker/sprice.html",{'price':sprice})

def sortbydate(request):                                    #sorting by date
    sdate=Item.objects.order_by('created_at').all()
    return render(request,"tracker/sdate.html",{'date':sdate})




def betweendate(request):
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        searchresult = Item.objects.filter(Q(created_at__gte=fromdate) & Q(created_at__lte=todate))
        searchresultcount = Item.objects.filter(Q(created_at__gte=fromdate) & Q(created_at__lte=todate)).count()
        d = {"searchresult" : searchresult , "fromdate" : fromdate , "todate" : todate , "searchresultcount" : searchresultcount}
        return render(request , "tracker/betweendate.html" , d)
    else:
        searchresult = Item.objects.all()
        return render(request , "tracker/betweendate.html" , {"searchresult":searchresult})



def news(request):
	if request.POST.get("src"):
		src = request.POST.get("src")
		try:

			a1 = "https://newsapi.org/v2/top-headlines"
			a2 = "?sources=" + src
			a3 = "&apikey=" + "dcf42dec7d614e778d3dcd8616ab8182"
			wa = a1+a2+a3
			res = requests.get(wa)
			data = res.json()
			info = data['articles']
			return render(request,"tracker/news.html",{"msg":info , "src":src})
		except Exception as e:
			return render(request,"tracker/news.html",{"msg":e})
	return render(request , "tracker/news.html")
