try:
    from .nonagentic.faq_generator_models import *
except ImportError:
    from app.FAQGenerator.nonagentic.faq_generator_models import *

from lite import ModelOutput
