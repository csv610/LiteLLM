import sys

from ..nonagentic import deep_deliberation_agents as _impl

sys.modules[__name__] = _impl
