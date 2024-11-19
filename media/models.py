from django.db import models,transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Type"
    

class Blog(models.Model):
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)   
    author = models.CharField(max_length=50) 


    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Blogs"

    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter_name} on {self.blog.title}"
from django.db import models

class Gallery(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    name = models.CharField(max_length=100)
    media = models.FileField(upload_to='media/')  # Handles both images and videos
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, default='image')  # To differentiate between media types

    def __str__(self):
        return self.name

    @property
    def media_url(self):
        try:
            return self.media.url
        except:
            return ''

    @property
    def is_image(self):
        """Check if the media is an image based on its type."""
        return self.media_type == 'image'

    @property
    def is_video(self):
        """Check if the media is a video based on its type."""
        return self.media_type == 'video'

    class Meta:
        verbose_name_plural = "Gallery"

from django.core.mail import send_mail
from django.db import models, transaction

class Booking(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('live stream', 'Live Stream'),
        ('video/photography', 'Video/Photography'),
        ('Event Planning', 'Event Planning'),
        ('Graphic Designing', 'Graphic Designing'),
        ('Gadget Rental', 'Gadget Rental'),
        ('MC', 'MC')
    ]
    PACKAGES =[
        ('Medium', 'Medium'),
        ('Full', 'Full'),
        ('Rental', 'Rental'),
        
    ]
    
    packges = models.CharField(max_length=20, choices=PACKAGES, default='Full1p')
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    event = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='live_stream')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.event} on {self.date} at {self.time}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            # Create a BookingStatus if it doesn't exist
            if not hasattr(self, 'status'):
                BookingStatus.objects.create(booking=self)

            # Send email after saving the booking
            send_mail(
                subject='New Booking Submitted',
                message=f"A new booking has been submitted:\n\n"
                        f"Packages: {self.packges}\n"
                        f"Name: {self.name}\n"
                        f"Service Type: {self.service_type}\n"
                        f"Address: {self.address}\n"
                        f"Event: {self.event}\n"
                        f"Date: {self.date}\n"
                        f"Time: {self.time}\n",
                from_email=self.email,  # Send from the user's email
                recipient_list=['ranchomhyc2019@gmail.com'],  # Replace with your recipient email(s)
                fail_silently=False,
            )

class BookingStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.name} - {self.get_status_display()}"
    class Meta:
        verbose_name_plural = "Booking Status"

class Radio_Comment(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:20]
class Program_Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    name = models.CharField(max_length=255)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/') 
    role = models.CharField(max_length=255)
    testimony= models.TextField(max_length=2000)
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
class Portfolio(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('live stream', 'Live Stream'),
        ('video/photography', 'Video/Photography'),
        ('Event Planning', 'Event Planning'),
        ('Graphic Designing', 'Graphic Designing'),
        ('Gadget Rental', 'Gadget Rental'),
        ('MC', 'MC')
    ]
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='live_stream')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/') 
   
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    

