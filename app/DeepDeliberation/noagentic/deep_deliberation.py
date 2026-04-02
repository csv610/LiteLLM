import sys

from ..nonagentic import deep_deliberation as _impl

sys.modules[__name__] = _impl
