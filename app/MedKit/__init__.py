# Lazy imports to avoid circular dependencies
# Only import when explicitly needed
try:
    from . import diagnostics
    from . import medical
except ImportError:
    # Allow tests to run without all modules available
    pass
