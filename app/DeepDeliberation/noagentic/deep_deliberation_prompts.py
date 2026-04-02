import sys

from ..nonagentic import deep_deliberation_prompts as _impl

sys.modules[__name__] = _impl
