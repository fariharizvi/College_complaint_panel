from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html   # ✅ REQUIRED
from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):

    # ==========================
    # LIST VIEW
    # ==========================
    list_display = (
        "title",
        "user",
        "category",
        "priority_display",
        "emotion_label",
        "status",
        "created_at",
    )

    list_filter = (
        "priority",
        "emotion_label",
        "status",
        "category",
    )

    search_fields = ("title", "description", "user__username")

    ordering = ("-created_at",)

    # ==========================
    # READ ONLY FIELDS
    # ==========================
    readonly_fields = (
        "user",
        "title",
        "category",
        "description",
        "stress_score",
        "emotion_label",
        "priority",
        "created_at",
    )

    # ==========================
    # PRIORITY DISPLAY (SAFE)
    # ==========================
    def priority_display(self, obj):
        if obj.priority == "Critical":
            return format_html('<b style="color:red;">Critical</b>')
        elif obj.priority == "High":
            return format_html('<b style="color:orange;">High</b>')
        elif obj.priority == "Medium":
            return format_html('<b style="color:#eab308;">Medium</b>')
        else:
            return format_html('<b style="color:green;">Low</b>')

    priority_display.short_description = "Priority"

    # ==========================
    # EMAIL NOTIFICATION
    # ==========================
    def save_model(self, request, obj, form, change):
        if change:
            subject = f"Complaint Update: {obj.title}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Priority: {obj.priority}
Emotion Detected: {obj.emotion_label}

Admin Reply:
{obj.reply or 'No reply provided yet.'}

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
