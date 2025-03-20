
try:
    import importlib.metadata as version_reader
except ImportError:
    import importlib_metadata as version_reader

try:
    __version__ = version_reader.version("sibi-dst")
except version_reader.PackageNotFoundError:
    __version__ = "unknown"

import importlib
import sys

def _load_module(version, module_name):
    # Construct the relative module path (e.g., ".v1.df_helper")
    module_path = f".{version}.{module_name}"
    #print(f"Loading module: {module_path} from package {__package__}")
    return importlib.import_module(module_path, package=__package__)


# Toggle version by setting the flag (or use an environment variable)
use_v2 = False
default_version = "v2" if use_v2 else "v1"

# Dynamically load the modules from the chosen version directory.
df_helper      = _load_module(default_version, "df_helper")
geopy_helper   = _load_module(default_version, "geopy_helper")
osmnx_helper   = _load_module(default_version, "osmnx_helper")
tests          = _load_module(default_version, "tests")
utils          = _load_module(default_version, "utils")

# Re-export the modules at the top level so that absolute imports work.
sys.modules[f"{__package__}.df_helper"]    = df_helper
sys.modules[f"{__package__}.geopy_helper"]   = geopy_helper
sys.modules[f"{__package__}.osmnx_helper"]   = osmnx_helper
sys.modules[f"{__package__}.tests"]          = tests
sys.modules[f"{__package__}.utils"]          = utils

# Define what is exported with "from sibi_dst import *"
__all__ = [
    "df_helper",
    "geopy_helper",
    "osmnx_helper",
    "tests",
    "utils"
]