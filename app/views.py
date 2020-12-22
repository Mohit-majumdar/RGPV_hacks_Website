from django.shortcuts import render, redirect,loader
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse
from wsgiref.util import FileWrapper


# Create your views here.
def home(request):  # For home page

    branch = Branch.objects.get(id=1)
    book = branch.book_set.all()
    civil = Branch.objects.get(id=2)
    civil_book = civil.book_set.all()
    mech = Branch.objects.get(id=3)
    mech_book = mech.book_set.all()

    # for semster
    sem = Semseter.objects.all()

# For notes
    user = request.user
    d = {'CSE': book, 'civil': civil_book, 'mech': mech_book, 'sem': sem,'user':user}
    if request.method == 'POST':

        suggetion_comment(request)




    return render(request, 'index.html', d)


def notes(request, string, sid):  # for Notes
    int(string)
    branch = Branch.objects.get(id=string)  # string is a id of branch which name is string
    sem = Semseter.objects.get(id=sid)
    notes = Notes.objects.filter(branch=branch, sem=sem)
    notes = list(notes)
    notes.reverse()

    downl = down(notes)
    z= zip(notes,downl)
    d = {'note': notes,'branch':branch,'d':z}

    return render(request, 'notes.html', d)

def down(note): #for the no. of downloads
    try:
        down = []
        b = 0
        for i in note:
            download = No_downloads.objects.filter(note=i)

            for j in download:
                b += j.downloads
            down.append(b)
            b = 0
        return down

    except Exception as e:
        return HttpResponse(e)
def download(request, nid=0, pid=0):
    int(nid)

    if int(pid) > 0:
        paper_object = Previous_year_question.objects.get(id=pid)
        paper = paper_object.file

        content = FileWrapper(paper)
        response = HttpResponse(content, content_type='application/pdf')
        response['content-disposition'] = 'attachment; filename=%s' % str(paper_object.name) + "-" + str(
            paper_object.year) + '.pdf'
        return response
    else:

        note_object = Notes.objects.get(id=nid)
        note = note_object.note
        no_of_download(note_object)
        content = FileWrapper(note)
        response = HttpResponse(content, content_type='application/pdf')
        response['content-disposition'] = 'attachment; filename=%s' % str(note_object.name) + '.pdf'
        return response


def book(request):  # for show notes
    sem = Semseter.objects.all()

    b = {'sem': sem}

    return render(request, 'index.html', b)


def Login(request):
    erorr = False

    if request.method == 'POST':
        n = request.POST['user']
        p = request.POST['pass']

        user = authenticate(username=n, password=p)

        if user:
            login(request, user)
            return redirect('user')
        else:
            erorr = True
    d = {'erorr': erorr}

    return render(request, 'login.html', d)


def Logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


def singup(request):
    erorr = False
    worng_password = False  # for worng entered password
    if request.method == 'POST':
        u = request.POST['user']
        e = request.POST['email']
        p = request.POST['pass']
        confirm_pasword = request.POST['confirm']
        num = request.POST['mobile']

        user = User.objects.filter(username=u)
        if user:
            erorr = True
        else:
            if p == confirm_pasword:
                u = User.objects.create_user(username=u, email=e, password=p)
                User_contect.objects.create(user=u, mobile=num)
                nuser = authenticate(username=u, password=p)

                login(request, nuser)
                return redirect('home')
            else:
                worng_password = True
                return redirect('singup')
    d = {'erorr': erorr, 'password': worng_password}
    return render(request, 'singup.html', d)


def order(request, oid):  # For order book

    if not request.user.is_authenticated():
        return redirect('login')

    if request.method == 'POST':
        to = request.user.email
        b = Book.objects.get(id=oid)
        u = request.user
        m = User_contect.objects.get(user=request.user)

        user_mobile = User_contect.objects.get(user=request.user)
        order = Order.objects.create(user=u, book=b, moblie=m)
        email(to, request.user.username, b.book, user_mobile, order)

        erorr = True

        return redirect('home')

    return render(request, 'order.html')


def email(To, name, titile, user_contect, order_id):  # for send email to group member
    from_email = settings.EMAIL_HOST_USER
    sub = 'Your book is confirm'
    sub1 = 'Here is a new book order'
    mas = EmailMultiAlternatives(sub, '', from_email, [To])
    msg = EmailMultiAlternatives(sub1, '', from_email,
                                 ['majumdarmohit12345@gmail.com', 'Sakshu0828@gmail.com', 'zehrashiza36@gmail.com',
                                  'lodhi5580@gmail.com'])
    # order krne bala user
    b = {'user': name, 'mobile': user_contect, 'order': order_id, 'book': titile}
    d = {'name': name, 'title': titile}
    html = get_template('mail.html').render(d)
    html1 = get_template('member_mail.html').render(b)  # for mail to member
    mas.attach_alternative(html, 'text/html')
    msg.attach_alternative(html1, 'text/html')
    mas.send()
    msg.send()


def suggetion_comment(request):  # for sgetion comments
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        comment = request.POST['Message']
        Suggetion_Comment.objects.create(name=name, email=email, massege=comment)


def privious_paper(request, bid, sid):
    branch = Branch.objects.get(id=bid)
    sem = Semseter.objects.get(id=sid)
    paper = Previous_year_question.objects.filter(branch=branch, sem=sem)
    print(paper)
    d = {"paper": paper}
    return render(request, 'paper.html', d)


def user_interface(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(user=request.user)
    notes = list(notes)
    notes.reverse()
    downl = down(notes)
    z = zip(notes,downl)
    return render(request,'dashbord.html',{'notes':z,'note':notes})
from datetime import date
def add_note(request):
    if not request.user.is_authenticated:
        return redirect('login')
    branchs = Branch.objects.all()
    s = Semseter.objects.all()
    d = {'branch':branchs,'sem':s}
    if request.method == "POST":
        name = request.POST['note']
        branch = request.POST['bid']
        sem = request.POST['sid']
        note = request.FILES['pdf']
        user = request.user
        b = Branch.objects.get(id = branch)
        sems = Semseter.objects.get(id = sem)
        d=date.today()


        n = Notes.objects.create(user=user,branch=b,sem=sems,name=name,note=note,date=d)
        No_downloads.objects.create(note=n, downloads = 0)

        return redirect('user')

    return render(request,'add_notes.html',d)


def add_paper(request):
    if not request.user.is_authenticated:
        return redirect('login')
    branchs = Branch.objects.all()
    s = Semseter.objects.all()
    d = {'branch': branchs, 'sem': s}
    if request.method == "POST":
        name = request.POST['note']
        branch = request.POST['bid']
        sem = request.POST['sid']
        paper = request.FILES['pdf']
        year = request.POST['year']
        user = request.user
        b = Branch.objects.get(id=branch)
        sems = Semseter.objects.get(id=sem)


        n = Previous_year_question.objects.create(user=user, branch=b, sem=sems, name=name, file=paper, year=year)


        return redirect('user')

    return render(request, 'add_paper.html', d)


def aboutus(request):
    return render(request,'aboutus.html')

def no_of_download(note):
    try:
        down = No_downloads.objects.filter(note=note).first()
    except:
        print(down)
    if down:
        down.downloads += 1
        down.save()
    else:
        No_downloads.objects.create(note=note, downloads = 1)


def test(request):
    user  = User.objects.get(id = request.user.id)
    print(user.password)

    return HttpResponse("password "+str(user.password))





