"""
Cache Manager Module for FinWise AI
Implements InMemoryCache and SQLiteCache for LangChain
"""
import os
from typing import Optional, Union

# Core cache imports
from langchain_core.caches import InMemoryCache

try:
    from langchain_community.cache import SQLiteCache
except ImportError:
    try:
        from langchain.cache import SQLiteCache
    except ImportError:
        # اگر پیکج موجود نہ ہو تو فال بیک کے طور پر InMemoryCache کام کرے گا
        SQLiteCache = InMemoryCache

from langchain_openai import ChatOpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL


class FinWiseCacheManager:
    def __init__(self, cache_type: str = "InMemoryCache"):
        self.cache_type = cache_type
        self.cache = None
        self._initialize_cache()

    def _initialize_cache(self):
        if self.cache_type == "SQLiteCache":
            cache_dir = "./.finwise_cache"
            os.makedirs(cache_dir, exist_ok=True)
            cache_path = os.path.join(cache_dir, "finwise_cache.db")
            try:
                self.cache = SQLiteCache(database_path=cache_path)
            except Exception:
                self.cache = InMemoryCache()
        else:
            self.cache = InMemoryCache()

    def set_llm_cache(self, llm: ChatOpenAI):
        if self.cache:
            llm.cache = self.cache

    def get_cache(self):
        return self.cache

    def clear_cache(self):
        if self.cache:
            if isinstance(self.cache, InMemoryCache):
                self.cache.clear()
            else:
                if hasattr(self.cache, 'database_path'):
                    cache_path = self.cache.database_path
                    if os.path.exists(cache_path):
                        os.remove(cache_path)

    def switch_cache(self, cache_type: str):
        if cache_type != self.cache_type:
            self.cache_type = cache_type
            self._initialize_cache()

    def get_cache_info(self) -> dict:
        info = {
            "cache_type": self.cache_type,
            "cache_class": type(self.cache).__name__ if self.cache else "None"
        }
        if hasattr(self.cache, 'database_path'):
            info["database_path"] = getattr(self.cache, 'database_path', 'Unknown')
        return info


def configure_cache_for_llm(
    llm: ChatOpenAI,
    cache_type: str = "InMemoryCache",
    cache_manager: Optional[FinWiseCacheManager] = None
) -> ChatOpenAI:
    """
    Applies cache configuration to an existing LLM instance.
    """
    if cache_manager is None:
        cache_manager = FinWiseCacheManager(cache_type=cache_type)
    cache_manager.set_llm_cache(llm)
    return llm


def create_cached_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    cache_type: str = "InMemoryCache"
) -> ChatOpenAI:
    if not model_name:
        model_name = OPENAI_MODEL

    cache_manager = FinWiseCacheManager(cache_type=cache_type)
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=model_name,
        temperature=temperature
    )
    cache_manager.set_llm_cache(llm)
    return llm


def get_cache_manager(cache_type: str = "InMemoryCache") -> FinWiseCacheManager:
    return FinWiseCacheManager(cache_type=cache_type)