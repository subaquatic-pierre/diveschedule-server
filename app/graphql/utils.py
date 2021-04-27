def get_viewer(info):
    user = info.context.user
    if not user.is_authenticated:
        raise PermissionException

    return user


def staff_permission_required(info):
    user = info.context.user
    if not user.is_authenticated:
        raise Exception("You are not logged in")

    if not user.is_staff:
        raise PermissionException

    return user


class PermissionException(Exception):
    def __init__(self):
        super().__init__("You do not have the correct permissions for the operation")
