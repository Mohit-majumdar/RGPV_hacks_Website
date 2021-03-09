from django.shortcuts import render,redirect
from .models import *
from  django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from random import randint

otp = 0
fuser = None
# Create your views here.
def home(request): # For home page
    branch = Branch.objects.get(id=1)
    book = branch.book_set.all()
    civil = Branch.objects.get(id=2)
    civil_book = civil.book_set.all()
    mech = Branch.objects.get(id=3)
    mech_book = mech.book_set.all()

    #for semster
    sem = Semseter.objects.all()

    #For notes

    d = {'CSE': book, 'civil': civil_book, 'mech': mech_book,'sem':sem}
    if request.method == 'POST':
        print("okkkk")
        suggetion_comment(request)

    return render(request,'index.html',d)
def notes(request,string,sid):              #for Notes
    int(string)
    branch = Branch.objects.get(id=string)   #string is a id of branch which name is string
    sem =  Semseter.objects.get(id = sid)
    notes = Notes.objects.filter(branch=branch,sem=sem)
    d={'note':notes}
    


    return render(request,'notes.html',d)

def download(request,nid=0,pid=0):
    int(nid)
    
    if int(pid)>0:
        paper_object = Previous_year_question.objects.get(id=pid)
        paper = paper_object.file

        content = FileWrapper(paper)
        response = HttpResponse(content,content_type='application/pdf')
        response['content-disposition'] ='attachment; filename=%s' % str(paper_object.name)+"-"+str(paper_object.year)+'.pdf'
        return response
    else:

        
        note_object = Notes.objects.get(id=nid)
        note = note_object.note

        content = FileWrapper(note)
        response = HttpResponse(content,content_type='application/pdf')
        response['content-disposition'] ='attachment; filename=%s' % str(note_object.name)+'.pdf'
        return response


def book(request): #for show notes
    sem = Semseter.objects.all()

    b = {'sem':sem}

    return render(request,'index.html',b)


def Login(request):
    erorr = False

    if request.method == 'POST':
        n = request.POST['user']
        p = request.POST['pass']

        user = authenticate(username=n,password=p)
        if user:
            login(request,user)
            return redirect('home')
        else:
            erorr = True
    d = {'erorr':erorr}

    return render(request,'login.html',d)


def Logout(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('login')

def singup(request):
    erorr = False
    worng_password =False #for worng entered password
    if request.method =='POST':
        u = request.POST['user']
        e = request.POST['email']
        p = request.POST['pass']
        confirm_pasword = request.POST['confirm']
        num = request.POST['mobile']

        user = User.objects.filter(username=u)
        if user:
            erorr = True
        else:
            if p ==confirm_pasword:
                u = User.objects.create_user(username=u, email=e, password=p)
                User_contect.objects.create(user = u, mobile= num )
                nuser = authenticate(username = u,password= p)

                login(request,nuser)
                return redirect('home')
            else:
                worng_password = True
                return redirect('singup')
    d = {'erorr': erorr, 'password':worng_password}
    return render(request,'singup.html',d)




def order(request,oid): # For order book

    if not request.user.is_authenticated():

        return redirect('login')

    if request.method == 'POST':
       
        to = request.user.email
        b = Book.objects.get(id=oid)
        u = request.user    
        m = User_contect.objects.get(user = request.user)

        user_mobile = User_contect.objects.get(user=request.user)
        order=Order.objects.create(user = u, book = b, moblie=m)
        email(to,request.user.username,b.book,user_mobile,order)


        erorr = True

        return  redirect('home')



    return render(request,'order.html')


def email(To,name,titile,user_contect,order_id):  # for send email to group member
    from_email = settings.EMAIL_HOST_USER
    sub = 'Your book is confirm'
    sub1 = 'Here is a new book order'
    mas = EmailMultiAlternatives(sub,'',from_email,[To])
    msg = EmailMultiAlternatives(sub1,'',from_email,['majumdarmohit12345@gmail.com','Sakshu0828@gmail.com','zehrashiza36@gmail.com','lodhi5580@gmail.com'])
     #order krne bala user
    b = {'user':name, 'mobile':user_contect,'order':order_id,'book':titile}
    d = {'name':name,'title':titile}
    html = get_template('mail.html').render(d)
    html1= get_template('member_mail.html').render(b) #for mail to member
    mas.attach_alternative(html,'text/html')
    msg.attach_alternative(html1,'text/html')
    mas.send()
    msg.send()
    
def suggetion_comment(request): #for sgetion comments
    # if request.method == 'POST':
    name = request.POST['Name']
    email = request.POST['Email']
    comment = request.POST['Message']
    Suggetion_Comment.objects.create(name=name,email=email,massege=comment)


def privious_paper(request,bid,sid):
    branch = Branch.objects.get(id=bid)
    sem = Semseter.objects.get(id=sid)
    paper = Previous_year_question.objects.filter(branch = branch, sem = sem)

    d = {"paper":paper}
    return render(request,'paper.html',d)

""" code for forget password """
def forget_password(request):
    user_not_found = False
    if request.method == "POST":
        email_ = request.POST["email"]

        user = User.objects.filter(email = email_).first()
        if user:
            global otp,fuser
            otp = randint(1000,9999)
            from_E = settings.EMAIL_HOST_USER   
            sub = "Your OTP "
            msg = EmailMultiAlternatives(sub,body=f"Your otp is {otp}",from_email= from_E,
            to = [email_])
            msg.send()
            fuser = user
            
            
            return redirect("enter_otp")

        else:
            user_not_found = True
        
    return render(request,"forget_passward.html",{"usernot":user_not_found})


def enter_opt(request):
    global otp
    worngOtp = False
    if request.method == "POST":
        uOtp = request.POST['otp']
        if int(uOtp) == otp:
            
            return redirect("enter_new_passward")
        else:
            worngOtp = True
            
    return render(request,"otp.html",{"worngotp":worngOtp})


def enter_new_passward(request):
    if request.method == "POST":
        pasw = request.POST['pass']
        fuser.set_password(pasw)
        fuser.save()
        

        return redirect('login')
    return render(request,"enter_password.html")

