from django.contrib import admin

from . models import *


admin.site.register(Contact)
# admin.site.register(Blog)
# admin.site.register(Comment)
# admin.site.register(Type)
admin.site.register(Gallery)
admin.site.register(Testimonial)
# admin.site.register(Portfolio)
# admin.site.register(Radio_Comment)
# @admin.register(Program_Schedule)
# class ProgramScheduleAdmin(admin.ModelAdmin):
#     list_display = ('name', 'day', 'start', 'end')

@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ('booking', 'status', 'updated_at')
    list_filter = ('status',)


