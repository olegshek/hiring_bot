from django.contrib import admin

from apps.hiring.models import Resume, HiringRequest, Category
from apps.hiring.signals import hiring_request_approved


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'approved')
    list_filter = ('user',)
    readonly_fields = (
        'resume_id',
        'user',
        'phone_number',
        'email',
        'category',
        'instagram',
        'education',
        'work_experience',
        'skills',
        'languages',
        'driver_license',
        'ready_for_business_trips',
        'additional_info',
        'photo',
        'filled_out_at',
        'created_at'
    )

    def get_queryset(self, request):
        return super(ResumeAdmin, self).get_queryset(request).filter(filled_out_at__isnull=False)


class HiringRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'resume', 'user', 'approved')
    list_filter = ('user', 'resume')
    readonly_fields = (
        'request_id',
        'user',
        'resume',
        'created_at',
        'message_id'
    )

    def save_model(self, request, obj, form, change):
        super(HiringRequestAdmin, self).save_model(request, obj, form, change)

        if 'approved' in form.changed_data and obj.approved:
            hiring_request_approved.send(sender=HiringRequest, instance=obj)


admin.site.register(Category)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(HiringRequest, HiringRequestAdmin)
