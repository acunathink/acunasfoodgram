def find_duplicates(obj_list, field_name):
    check_ids = {}
    duplicates = []
    for check_obj in obj_list:
        if check_obj.id not in check_ids:
            check_ids[check_obj.id] = check_obj
        else:
            duplicates.append(check_obj)
    return duplicates
