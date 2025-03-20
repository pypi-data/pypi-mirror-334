from importlib import metadata

from langchain_xinference.chat_models import ChatXinference
from langchain_xinference.llms import Xinference


try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ChatXinference",
    "Xinference",
    "__version__",
]
