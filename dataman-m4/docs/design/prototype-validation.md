# Prototype validation

Run from the prototype folder:

```text
python -m unittest discover -s tests -v
```

The tests check correct first/second answers, two incorrect answers, separate
attempt history, no premature reveal, rejection of a third answer, invalid
input without consuming a try, rejection of an eleventh set member at both
logic and storage boundaries, and the limits of in-memory session state.

The text interface is also exercised with piped inputs for the main branches.
Executed on November 23, 2026 (America/New_York): all 6 automated tests passed.
The real text entry point also passed 5 subprocess checks: two misses (50,
54), correct first (56), correct second (50, 56), invalid input (abc, 56), and
quit (q). The two-miss run requested exactly two answers, displayed Try 1 of 2
and Try 2 of 2, then revealed 56 and recorded two attempts.

The persistent-recovery requirement remains unresolved. A test deliberately
confirms that a new MemoryStore has no old session. This documents the stub's
limit and does not count as successful recovery.
