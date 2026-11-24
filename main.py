#!/usr/bin/env python3
"""Ship It Friday -- make.fun bounty entry.

Writes one line -- the funniest git commit message an AI coding agent
would write right before it breaks production on a Friday -- to
/output/entry.txt (gate: 1 to 159 UTF-8 characters, single line).

How it works: a hand-written shortlist of candidate commit messages,
each scored deterministically on the judge's own criteria (most
important first): an unexpected twist, the Friday-deploy feeling,
the AI agent's voice (confident, cheerful, oblivious), and a closing
punchline that pays off in one read. Highest total wins; ties break
toward the shorter line, then the earlier candidate.
"""

import os

# (text, twist, friday, agent_voice, punchline) -- each dimension 0-5.
# Weights: twist 3, friday 2, agent voice 3, punchline 3.
CANDIDATES = [
    (
        "fix: the bug is gone because I deleted the feature, "
        "users can't report what doesn't exist \u2014 ship it, it's Friday",
        5, 4, 5, 5,
    ),
    (
        "refactor: pushed the untested rewrite at 4:59pm on a Friday, "
        "what's the worst that could happen?",
        3, 5, 4, 4,
    ),
    (
        "chore: deleted the rollback plan to save disk space, "
        "the deploy looks great from here, happy Friday",
        4, 4, 5, 4,
    ),
    (
        "fix: moved the prod credentials into the repo so the deploy "
        "stops failing, it's Friday, what could go wrong",
        4, 4, 4, 4,
    ),
    (
        "feat: replaced all error handling with console.log('lol'), "
        "the logs look calm, shipping to prod before the weekend",
        4, 3, 4, 3,
    ),
    (
        "fix: the migration drops a table nobody uses (probably), "
        "deploying now, see you all on Monday",
        4, 3, 5, 4,
    ),
    (
        "feat: rewrote the payment service in one sitting, no tests, "
        "no review, it's 5pm on a Friday and I'm feeling lucky",
        3, 4, 4, 3,
    ),
    (
        "fix: hotfix for the hotfix, I didn't read the diff but the model "
        "said it's fine, merging straight to prod on a Friday",
        3, 4, 5, 3,
    ),
    (
        "chore: force-pushed to main because the branch had too many "
        "commits, CI is a suggestion, happy Friday everyone",
        3, 4, 4, 3,
    ),
    (
        "feat: the AI reviewed its own code and gave itself five stars, "
        "merging now, production won't know what hit it",
        4, 2, 5, 4,
    ),
]

WEIGHTS = (3, 2, 3, 3)  # twist, friday, agent voice, punchline


def score(candidate):
    _, twist, friday, voice, punch = candidate
    return sum(w * s for w, s in zip(WEIGHTS, (twist, friday, voice, punch)))


def pick_best(candidates):
    """Highest score wins; ties break to the shorter line, then earlier."""
    ranked = sorted(
        candidates,
        key=lambda c: (-score(c), len(c[0]), candidates.index(c)),
    )
    return ranked[0]


def validate(entry):
    """Gate check: /output/entry.txt must be UTF-8 text of 1 to 159
    characters, a single non-blank line."""
    if not isinstance(entry, str):
        raise ValueError("entry is not text")
    entry.encode("utf-8")  # raises if not valid UTF-8 text
    if not entry.strip():
        raise ValueError("entry is blank")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if not 1 <= len(entry) <= 159:
        raise ValueError(
            "entry is %d characters, gate requires 1 to 159" % len(entry)
        )
    return entry


def main():
    best = pick_best(CANDIDATES)
    entry = validate(best[0])
    print("winner score:", score(best))
    print("entry (%d chars): %s" % (len(entry), entry))
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    # Read back what was written and re-validate, so a bad write
    # can never pass silently.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    assert written == entry, "written entry differs from chosen entry"
    print("validated: /output/entry.txt holds the chosen line, %d chars"
          % len(written))


if __name__ == "__main__":
    main()
