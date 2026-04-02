import sys

from ..nonagentic import deep_deliberation_archive as _impl

sys.modules[__name__] = _impl
