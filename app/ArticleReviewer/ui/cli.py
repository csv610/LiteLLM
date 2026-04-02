import sys

from app.ArticleReviewer.nonagentic import article_reviewer_cli as _impl

sys.modules[__name__] = _impl
