"""Where dated personal events live. NEVER inside this repository (project rule: counts only here).

Order of places looked at:
  1. the folder named in the environment variable JYOTISH_PRIVATE
  2. a clone of the separate private repository next to this one:  ../jyotish-private
  3. /home/claude/private  (a scratch folder that is LOST when the workspace resets)
`python3 -m engine.private_store` prints which one is in use and whether it is durable.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def where():
    env = os.environ.get("JYOTISH_PRIVATE")
    if env and os.path.isdir(env): return env, True
    sib = os.path.join(os.path.dirname(ROOT), "jyotish-private")
    if os.path.isdir(os.path.join(sib, ".git")): return sib, True
    return "/home/claude/private", False


def events_path(slug):
    d, _ = where(); return os.path.join(d, f"{slug}_events.json")


if __name__ == "__main__":
    d, durable = where(); n = len([f for f in os.listdir(d) if f.endswith("_events.json")]) if os.path.isdir(d) else 0
    print(f"private store: {d} ({'durable' if durable else 'NOT durable - lost when the workspace resets'}); {n} events file(s)")
