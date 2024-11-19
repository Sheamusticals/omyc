
from django.shortcuts import render ,get_object_or_404,redirect
from .forms import *
from .models import *
from django.db.models import Count
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib import messages

@receiver(post_save, sender=Booking)
def create_booking_status(sender, instance, created, **kwargs):
    if created:
        BookingStatus.objects.create(booking=instance)

def index(request):
    testimonials = Testimonial.objects.all()
    portfolios = Portfolio.objects.all()
    context ={'testimonials':testimonials,'portfolios':portfolios}
    return render(request,'index.html',context)

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Add success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the contact page
        else:
            # Render the form with errors
            return render(request, 'contact_us.html', {'form': form})
    else:
        # Handle GET request by rendering the form
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})

def blog(request):
    blogs = Blog.objects.all().order_by('-date')

    archive_dates = Blog.objects.annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(count=Count('id')).order_by('-year', '-month')

    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = RadioForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
      
            comment.save()
            return redirect('blog')
    else:
        form = RadioForm()

    comments = Radio_Comment.objects.all()
    schedules = Program_Schedule.objects.all()
    types = Type.objects.all()
    context = {
        'page_obj': page_obj,
        'types': types,
        'archive_dates': archive_dates,
        'comments':comments,
        'form':form,
        'schedules':schedules
    }
    


    return render(request, 'blog.html', context)


def post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return JsonResponse({'success': True})
        else:
     
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)


    form = CommentForm()
    return render(request, 'post.html', {'blog': blog, 'form': form, 'comments': comments})

def blog_by_type(request, type_id):
    blog_type = get_object_or_404(Type, pk=type_id)
    blogs = Blog.objects.filter(type=blog_type).select_related('type').order_by('-date')

    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blog_type': blog_type,
        'page_obj': page_obj,
    }
    return render(request, 'blog_by_type.html', context)


def archive(request, year=None, month=None):
    blogs = Blog.objects.all()
    
    paginator = Paginator(blogs,12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if year is not None and month is not None:
        archive_dates = Blog.objects.filter(date__year=year, date__month=month).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    elif year is not None:
        archive_dates = Blog.objects.filter(date__year=year).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    else:
        archive_dates = Blog.objects.annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    


  
    context = {'archive_dates': archive_dates, 'blogs': blogs,'page_obj':page_obj}
    return render(request, 'archive.html', context)
def gallery(request):
    galleries = Gallery.objects.all()
    context ={'galleries':galleries}


    return render(request,'gallery.html',context)
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import BookingForm
from .models import BookingStatus
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.save()

            # Check or create BookingStatus
            booking_status, created = BookingStatus.objects.get_or_create(
                booking=booking_instance,
                defaults={'status': 'pending'}
            )
            if not created:
                booking_status.status = 'pending'
                booking_status.save()

            # Send email notification
            try:
                send_mail(
                    subject='New Booking Submitted',
                    message=f"A new booking has been submitted:\n\n"
                            f"Packages: {booking_instance.packges}\n"
                            f"Name: {booking_instance.name}\n"
                            f"Contact: {booking_instance.contact}\n"
                            f"Service Type: {booking_instance.service_type}\n"
                            f"Address: {booking_instance.address}\n"
                            f"Event: {booking_instance.event}\n"
                            f"Date: {booking_instance.date}\n"
                            f"Time: {booking_instance.time}\n",
                    from_email=booking_instance.email,
                    recipient_list=['ranchomyc2019@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "Form submitted, but email notification failed. Please contact us directly.")
            else:
                messages.success(request, "Form submitted successfully!")

            return render(request, 'booking.html', {'form': BookingForm()})
        else:
            return render(request, 'booking.html', {'form': form})

    return render(request, 'booking.html', {'form': BookingForm()})
def pricing(request):
    return render(request,'pricing.html')
