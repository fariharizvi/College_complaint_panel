from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint
from django.db.models import Case, When, Value, IntegerField
from django.utils.html import format_html



class ComplaintAdmin(admin.ModelAdmin):
    # 🔹 OLD CODE (kept)
    list_display = ['title', 'user', 'status', 'created_at']

    # 🔹 NEW: add priority & psychological info to admin list
    list_display += ['colored_priority', 'emotion_label', 'stress_score']

    list_editable = ['status']
    readonly_fields = ['user', 'title', 'description', 'created_at']
    fields = [
        'user',
        'title',
        'description',
        'status',
        'priority',
        'stress_score',
        'emotion_label',
        'reply',
        'created_at'
    ]

    def colored_priority(self, obj):
        color_map = {
            "Critical": "red",
            "High": "orange",
            "Medium": "gold",
            "Low": "green",
        }
        color = color_map.get(obj.priority, "black")
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.priority
        )

    colored_priority.short_description = "Priority"


    # 🔹 NEW: priority-based ordering logic
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            priority_order=Case(
                When(priority='Critical', then=Value(1)),
                When(priority='High', then=Value(2)),
                When(priority='Medium', then=Value(3)),
                When(priority='Low', then=Value(4)),
                output_field=IntegerField(),
            )
        ).order_by('priority_order', '-created_at')

    # 🔹 OLD CODE (kept)
    def save_model(self, request, obj, form, change):
        if change:  # Only send email if it's an update
            subject = f"Complaint Update: {obj.title}"
            message = f"""
Hello {obj.user.username},

Your complaint has been updated.

Status: {obj.status}
Priority: {obj.priority}
Reply: {obj.reply or 'No reply'}

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
