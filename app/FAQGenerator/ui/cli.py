import sys

from app.FAQGenerator.nonagentic import faq_generator_cli as _impl

sys.modules[__name__] = _impl
