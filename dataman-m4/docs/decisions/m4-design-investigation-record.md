# M4 Design Investigation Record

## Product Slice
Check an Answer with feedback and a second attempt.

## Initial Question
What should happen after the learner's first and second incorrect answers, and when should the correct answer be shown?

## Planned Evidence
A behavior flow, a state table, and sample text screens for correct and incorrect answers.

## Evidence Actually Used
- Use-case boundary / actor-goal framing
- Behavior/state flow and two-attempt simulation
- Data-model/schema and Memory Bank constraint stress tests
- Interface/wireframe comparison and state audit
- Design complication and critique

## Findings
### Use-Case Boundary / Question Framing
Learner → check an answer and understand the result.

Design question: What feedback should the learner see after the first wrong answer so they know they can try again?

### Behavior / State
The first wrong answer should show EEE and allow another attempt without revealing the answer. The second wrong answer should show EEE and then reveal the correct answer. A correct first answer should finish the problem without a retry.

### Data / Persistence
The data model showed that each attempt needs its own record so the first and second answers are not overwritten. It also showed the need for practice-set membership, saved session results, and a ten-problem limit.

### Memory Bank Constraint
The eleventh problem could not be added. The business logic should enforce the ten-problem limit and keep the existing problems unchanged.

**Constraint boundary selected:** both

### Interaction
Approach A does not explain EEE or show the attempt number. Approach B makes the attempt visible, but it shows Retry on try 2 of 2. The interface should allow retry only after the first wrong answer and reveal the answer after the second wrong answer. Curator review needs a separate history view with session results and individual attempts.

## Layer Boundary Notes
**Business behavior that should remain outside the interface:**
Checking the answer, tracking the attempt number, deciding whether a retry is allowed, and deciding when to reveal the correct answer should be handled by the business logic.

**Data that can be stubbed now:**
The prototype can keep problems, attempts, practice sets, and session results in lists or dictionaries in memory. A separate store module should handle saving and retrieving them so persistent storage can replace it later. This temporary storage will not preserve progress after the program closes.

## New Complication
**Response:** Revise state boundary

The two-attempt rule needs the first attempt to remain available after the program closes. Earlier requirements also call for preserving progress after interruptions. Attempt and session state should be saved outside the interface so reopening does not reset the learner to try 1.

## Build-Readiness Decision
**Disposition:** Revise

**Design decision:**
Revise the design so business logic controls attempts, retries, and answer reveal. Store attempt and session state outside the interface, and add persistent storage before claiming support for recovery after closing.

## Revision From Initial Thinking
I first planned to use temporary in-memory storage. The interruption scenario showed that this would lose the first attempt when the program closes. The interface also needs to show Retry only when another attempt is allowed.

## Tradeoff Accepted
The text prototype will use a replaceable in-memory store to test the two-attempt behavior. Recovery after closing remains unfinished and will be documented as a limitation.

## Unresolved Uncertainty
Persistent recovery still needs to be implemented and tested. The rules for which curators may view a learner's history also need clarification.

## Next Question
What session and attempt data must be saved so reopening after the first wrong answer restores try 2 without losing history or allowing an extra attempt?

## Three-Layer Prototype Bridge
Text interface: display the problem, attempt number, feedback, and available next action, and receive learner input.

Business logic: check answers, control the two-attempt rule, allow retry after the first wrong answer, reveal the answer after the second wrong answer, and enforce the ten-problem limit.

Stubbed data layer: keep problems, practice sets, sessions, and separate attempt records in memory through replaceable save and retrieve functions. Data will be lost when the program closes, so persistent recovery remains unfinished.

## Trace Back to Product Work
This slice supports answer feedback and repeated practice. Proposed acceptance criteria: a correct answer shows success; the first wrong answer allows one retry; the second wrong answer shows the correct answer. Links to existing requirement and story IDs still need to be confirmed.
