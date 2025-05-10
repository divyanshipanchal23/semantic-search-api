import warnings
import pytest

# Filter out Pydantic deprecation warnings
def pytest_configure(config):
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
    warnings.filterwarnings("ignore", message="Support for class-based `config` is deprecated", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*Support for class-based `config` is deprecated.*", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*model_.*_v1 attributes have been deprecated.*", category=DeprecationWarning) 