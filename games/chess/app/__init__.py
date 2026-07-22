"""Chess APPLICATION layer -- orchestration.

Ties the pure domain to concrete players and drives the flow of a game.
This is where the "turns alternate" assumption lives (Session) -- deliberately
NOT in the domain, so a real-time variant (Kung Fu) can add a different driver
without touching the rules.

Dependency rule: app/ imports domain/ only. Never pygame, never ui/.
(The AI's multiprocessing lives here, but it passes plain domain objects.)
"""
