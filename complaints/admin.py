from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "created_at")
    readonly_fields = ("user", "title", "category", "description")

    # ✅ Properly indented inside the class
    def save_model(self, request, obj, form, change):
        if change:  # Send email only on update
            subject = f"Complaint Update: {obj.title}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Reply: {obj.reply or 'No reply provided yet.'}

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
