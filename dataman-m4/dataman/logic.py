"""Reusable rules. No input(), print(), or dependence on a text interface."""


class AnswerChecker:
    def __init__(self, store):
        self.store = store

    def start_session(self, learner_id, set_id):
        problem_ids = self.store.get_set(set_id)
        if not problem_ids:
            raise ValueError("Choose a practice set with at least one problem.")
        return self.store.create_session({
            "learner_id": learner_id, "set_id": set_id,
            "problem_ids": problem_ids, "position": 0,
            "try_number": 1, "finished": False, "solved": 0,
        })

    def get_state(self, session_id):
        session = self.store.get_session(session_id)
        state = {"finished": session["finished"]}
        if not session["finished"]:
            problem = self.store.get_problem(session["problem_ids"][session["position"]])
            # Do not expose the answer before the reveal rule allows it.
            state.update(prompt=problem["prompt"], try_number=session["try_number"])
        return state

    def submit_answer(self, session_id, submitted_answer):
        if type(submitted_answer) is not int:
            raise ValueError("An answer must be a whole number.")
        session = self.store.get_session(session_id)
        if session["finished"]:
            raise ValueError("This session is already complete.")
        problem_id = session["problem_ids"][session["position"]]
        problem = self.store.get_problem(problem_id)
        correct = submitted_answer == problem["answer"]
        try_number = session["try_number"]
        self.store.add_attempt({
            "session_id": session_id, "learner_id": session["learner_id"],
            "problem_id": problem_id, "try_number": try_number,
            "submitted_answer": submitted_answer, "correct": correct,
        })
        retry_allowed = not correct and try_number == 1
        result = {"correct": correct, "retry_allowed": retry_allowed,
                  "try_number": try_number}
        if retry_allowed:
            session["try_number"] = 2
        else:
            if correct:
                session["solved"] += 1
            else:
                result["answer"] = problem["answer"]
            session["position"] += 1
            session["try_number"] = 1
            session["finished"] = session["position"] == len(session["problem_ids"])
        self.store.save_session(session_id, session)
        if session["finished"]:
            self.store.save_result(session_id, {
                "total": len(session["problem_ids"]), "solved": session["solved"],
                "attempts": len(self.store.get_attempts(session_id)),
            })
        return result

    def get_summary(self, session_id):
        if not self.store.get_session(session_id)["finished"]:
            raise ValueError("The session is not complete.")
        return self.store.get_result(session_id)

    def add_problem_to_set(self, set_id, problem_id):
        problem_ids = self.store.get_set(set_id)
        if len(problem_ids) >= 10:
            raise ValueError("A practice set can contain at most ten problems.")
        if problem_id in problem_ids:
            raise ValueError("This problem is already in the set.")
        self.store.get_problem(problem_id)
        self.store.save_set(set_id, problem_ids + [problem_id])
