from django.conf.urls import url
from django.contrib import admin
from app.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^user/$',user_interface,name="user"),
    url(r'^admin/', admin.site.urls),
    url(r'^$',home,name='home'),
    url(r'^book/$',book,name='book'),
    url(r'^login/$',Login,name='login'),
    url(r'^Logout/$',Logout,name='logout'),
    url(r'singup/$',singup,name='singup'),
    url(r'order/(?P<oid>[0-9]+)/$',order,name='order'),
    url(r'^book/notes/(?P<string>[\w-]+)/(?P<sid>[0-9]+)/$',notes,name='notes'),
    url(r'^book/note/downlod/(?P<nid>[0-9]+)/(?P<pid>[0-9])/$',download,name='download'),
    url(r'^previous/(?P<bid>[0-9]+)/(?P<sid>[0-9]+)/$',privious_paper,name="paper"),
    url(r'^addnote/$',add_note,name="add_note"),
    url(r'add_paper/$',add_paper,name="q_paper"),
    url(r'^aboutUs/$',aboutus,name= "about us"),
    url(r'test',test),
    url(r'forgetpassward/$',forget_password, name='frogetPass'),
    url(r'enter_otp/$',enter_opt,name="enter_otp"),
    url(r'^enter_otp/enter_new_passward/$',enter_new_passward,name="enter_new_passward")


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
