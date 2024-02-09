from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import ValidationError


def find_duplicates(obj_list, field_name):
    check_ids = {}
    duplicates = []
    for check_obj in obj_list:
        if check_obj.id not in check_ids:
            check_ids[check_obj.id] = check_obj
        else:
            duplicates.append(check_obj)
    return duplicates


def get_object_or_validation_error(model, pk, err_str):
    try:
        obj = model.objects.get(pk=int(pk))
    except ObjectDoesNotExist as exc:
        raise ValidationError(err_str) from exc
    return obj
