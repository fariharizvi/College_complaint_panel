from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at']
    list_editable = ['status']
    readonly_fields = ['user', 'title', 'description', 'created_at']
    fields = ['user', 'title', 'description', 'status', 'admin_reply', 'created_at']

    def save_model(self, request, obj, form, change):
        if change:  # Only send email if it's an update
            subject = f"Complaint Update: {obj.subject}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Reply: {obj.admin_reply or 'No reply'}

Regards,
Complaint Management System
"""

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [obj.user.email],
                fail_silently=True,
            )

        super().save_model(request, obj, form, change)


admin.site.register(Complaint, ComplaintAdmin)
