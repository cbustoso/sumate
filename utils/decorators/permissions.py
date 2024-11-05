def is_administrator(user):
    return user.groups.filter(name='administrator').exists()

def is_student(user):
    return user.groups.filter(name='student').exists()