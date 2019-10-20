# service/resource/project/utils/paint


class Paint:
    """ Use in 'flask.blueprint', for spliting routes.

        :param prefix(str): always start with slash, as rule's prefix
            default is None.
    """
    def __init__(self, prefix=None):
        self.prefix = '' if prefix is None else prefix
        self.container = []
        self.class_container = []

    def route(self, rule, **kwargs):
        """Keep route informations"""
        def decorator(func):
            endpoint = kwargs.pop('endpoint', func.__name__)
            self.container.append((endpoint, rule, func, kwargs))

        return decorator

    def depict(self, blueprint):
        """Register route on blueprint"""
        for (endpoint, rule, f, kwargs) in self.container:
            blueprint.add_url_rule(
                ''.join((self.prefix, rule)),
                endpoint, f, **kwargs
            )
