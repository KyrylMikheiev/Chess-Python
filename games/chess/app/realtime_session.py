"""Real-time session driver (Kung Fu Chess) -- LATER, do not build speculatively.

Placeholder to make the architecture's intent explicit: when you build Kung Fu,
its "no turns, pieces move with cooldowns" nature lives HERE, as a different
driver, reusing the SAME domain primitives (movegen.is_legal-style checks and
movegen.apply). The rules layer barely changes; only the flow does.

Delete this note and implement only when you actually start Kung Fu.
"""
from __future__ import annotations

# TODO (only when building Kung Fu): a driver that, instead of alternating,
# tracks per-piece cooldown timers and applies moves as they are issued.
