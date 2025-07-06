from django.contrib import admin
from .models import Complaint
from django.core.mail import send_mail
from django.conf import settings

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'status', 'date_submitted']
    list_editable = ['status']
    readonly_fields = ['user', 'subject', 'description', 'date_submitted']
    fields = ['user', 'subject', 'description', 'status', 'admin_reply', 'date_submitted']

    def save_model(self, request, obj, form, change):
        if change:  # Only send email if it's an update
            subject = f"Complaint Update: {obj.subject}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Reply: {obj.admin_reply or 'No reply'}

Regards,
College Complaint System
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.user.email])

        super().save_model(request, obj, form, change)
