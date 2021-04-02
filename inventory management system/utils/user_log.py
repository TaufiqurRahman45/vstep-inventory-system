from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.models import LogEntry, CHANGE
from django.utils.encoding import force_text


def create_log(request, obj, flag=CHANGE):
    """
        Log that an object has been successfully changed.
    """
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=force_text(obj),
        action_flag=CHANGE
    )
