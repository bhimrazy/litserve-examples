import os
from collections import OrderedDict
from typing import Any

# States to keep; 0 disables the cache entirely.
CACHE_SIZE = int(os.environ.get("KEV_PREFIX_CACHE", "4"))
# Below this many state tokens the branch-only pass is not worth the bookkeeping.
MIN_TOKENS = int(os.environ.get("KEV_PREFIX_MIN_TOKENS", "384"))


class PrefixCache:
    """LRU cache of Kev state prefixes, keyed by the state's tokens.

    Kev reads the state once and then answers each question from its own
    branch. Everything up to the first question therefore has
    activations that do not depend on the questions, so a repeated state
    can reuse them and pay only for its branches. Reuse is exact, not
    approximate.

    Upstream keeps this in a module-global dict; holding it on an
    instance gives each LitServe worker its own.
    """

    def __init__(self, size: int = CACHE_SIZE, min_tokens: int = MIN_TOKENS):
        self.size = size
        self.min_tokens = min_tokens
        self.hits = 0
        self.misses = 0
        self._prefixes: OrderedDict[Any, Any] = OrderedDict()

    def probs(self, model: Any, enc: dict) -> tuple[Any, bool]:
        """Score an encoded request, reusing the state prefix when possible.

        Args:
            model: The loaded Kev model.
            enc: The encoding returned by ``model.encode``.

        Returns:
            The per-question probabilities, and whether the prefix was cached.
        """
        state_len = enc["seg"].count(0)
        if not self.size or state_len < self.min_tokens:
            return model.probs(enc), False

        key = (tuple(enc["ids"][:state_len]), bool(enc.get("option_isolation")))
        if key in self._prefixes:
            self._prefixes.move_to_end(key)
            self.hits += 1
            return model.probs_with_prefix(enc, self._prefixes[key]), True

        probs, prefix = model.probs_and_prefix(enc)
        self._prefixes[key] = prefix
        while len(self._prefixes) > self.size:
            self._prefixes.popitem(last=False)
        self.misses += 1
        return probs, False
