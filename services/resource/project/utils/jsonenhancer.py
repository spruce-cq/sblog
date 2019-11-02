# services/resource/project/utils/jsonenhancer.py


def toDict(obj):
    if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
        return dict(obj)
