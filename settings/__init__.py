try:
    from .development import *
except ImportError:
    from .deployment import *
