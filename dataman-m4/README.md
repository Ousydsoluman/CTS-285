# DataMan M4 Text Prototype

## Selected slice and question

The learner checks an answer with feedback and a second attempt.
Question: what happens after the first and second wrong answers, and when is the answer revealed?

## Run

Use Python 3. No packages need to be installed.

```text
python app.py
```

The demo asks `7 x 8`. Enter `50`, then `54` to see both incorrect attempts.
Run again and enter `56` to test a correct first answer. Run again and enter
`50`, then `56` to test a correct second answer. Enter `abc` to test invalid
input, or `q` to leave.

## Three layers

| Layer          | File             | Responsibility                                                           |
| -------------- | ---------------- | ------------------------------------------------------------------------ |
| Text interface | app.py           | Input, output, readable feedback and available next action               |
| Business logic | dataman/logic.py | Answer checking, attempt count, retry/reveal rules, ten-problem limit    |
| Stubbed data   | dataman/store.py | Problems, set membership, sessions, separate attempts, completed results |

The logic can run without the text interface. Storage is passed into the logic
so a persistent implementation can replace MemoryStore later.

## Acceptance criteria and traceability

These are proposed criteria from the supplied M4 Design Investigation Record,
not invented IDs from an earlier backlog. Existing Module 2 requirement and
Module 3 story IDs are still unconfirmed. Add those links when available.

| Local criterion | Expected behavior                                                    | Verification                                                  |
| --------------- | -------------------------------------------------------------------- | ------------------------------------------------------------- |
| AC-1            | Correct first answer completes the problem                           | test_correct_first_try_finishes                               |
| AC-2            | First wrong answer allows one retry without revealing the answer     | test_two_misses_preserve_history_and_reveal_only_after_second |
| AC-3            | Second wrong answer reveals the correct answer and stops retries     | same test; third submission rejected                          |
| AC-4            | Correct second answer completes the problem                          | test_correct_second_try                                       |
| AC-5            | Separate attempt records preserve both submitted answers             | two-miss history assertions                                   |
| AC-6            | An eleventh set member is rejected without changing the original ten | test_eleventh_problem_rejected_without_changing_set           |

## Evaluation and revision

The Studio flow check reported that reveal was gated behind the second miss.
The relationship inspection reported that history was preserved, problems
could be reused, and set membership could be counted. The wireframe showed
Retry on Try 2 of 2; this prototype removes that action after the second miss.
The interface receives retry/reveal decisions from the logic rather than
deciding them independently.

Each attempt is saved separately. The prototype summarizes problems solved
within two tries; this is a local demonstration count, not a confirmed final
DataMan scoring policy. Invalid whole-number input is rejected without using
an attempt, a provisional usability choice.

See docs/design/prototype-validation.md for executed checks and limits.

## Intentional stubs and unfinished work

- Data is in memory only. Closing the process loses progress and history.
- Recreating the interface/service with the same store preserves state only
  while the process remains alive; this is not cross-session recovery.
- No login, curator permissions, persistent database, or curator history UI.
- One fixed multiplication problem keeps the runnable slice small. Set-size
  rules are exercised directly by tests, outside the text interface.
- This prototype tests a narrowed core. The full progress-preservation
  requirement is unfinished and must not be marked complete.
- The M4 Lab Evidence Record and earlier backlog were not supplied. This
  package does not claim to replace those assignments or report unseen labs.

## Next implementation question

What attempt/session data and reliable write operation are needed to restore
Try 2 after closing, without losing history or allowing an extra attempt?
Curator access rules also need clarification before history is exposed.

## Files to add to the course repository

Copy these files into the existing CTS-285 repository, preserving its current
files. Also place the downloaded original Studio record at
`docs/decisions/m4-design-investigation-record.md`.
Submit the direct GitHub URL to the prototype location, according to Canvas.
The ZIP is a transfer package, not the required Canvas submission URL.
