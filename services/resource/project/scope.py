# service/resource/project/scope.py


class Scope:
    allow_api = set()
    # allow_redprint = set()  #可以通过RedPrint来实现基于此的模块控制


class UserScope(Scope):
    allow_api = {
        'users.logout_user',
        'users.get_user_status',
        'blog.add_category',
        'blog.delete_single_category',
        'blog.add_article',
        'blog.update_single_article',
    }


class AdminScope(Scope):
    allow_api = {
        'users.add_user',
        'blog.delete_single_article'
    }

    def __init__(self):
        self.allow_api = self.allow_api | UserScope().allow_api


def endpoint_in_scope(endpoint, scope='UserScope'):
    """Determine if the endpoint is in the scope.

    :param endpoint the flask endpoint of view_func
    :param scope(str): the user's power scope, default is `UserScopoe`
    :return: None if endpoint in scope, else raise APIException - Forbidden.
    """
    if endpoint in globals()[scope]().allow_api:
        return True
    else:
        return False
