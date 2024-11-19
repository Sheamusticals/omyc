from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('contact_us/',views.contact_us,name='contact'),
    path('blog/',views.blog,name='blog'),
    path('post/<int:blog_id>/', views.post, name='post'),
    path('blog/type/<int:type_id>/', views.blog_by_type, name='blog_by_type'),
    path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    path('gallery/',views.gallery,name='gallery'),
    path('booking/',views.booking,name='booking'),
    path('pricing/',views.pricing,name='pricing'),
]