# services/resource/project/utils/jsonenhancer.py


def toJSON(obj):
    if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
        return dict(obj)
