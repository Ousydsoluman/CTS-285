"""Replaceable storage stub; no files or database are written."""
from copy import deepcopy


class MemoryStore:
    def __init__(self):
        self.problems = {"p1": {"problem_id": "p1", "prompt": "7 x 8 = ?", "answer": 56}}
        self.practice_sets = {"demo-set": ["p1"]}
        self.sessions = {}
        self.attempts = []
        self.results = {}

    def get_problem(self, problem_id):
        return deepcopy(self.problems[problem_id])

    def get_set(self, set_id):
        return list(self.practice_sets[set_id])

    def save_set(self, set_id, problem_ids):
        # Storage support for the same limit checked by business logic.
        if len(problem_ids) > 10:
            raise ValueError("A practice set can contain at most ten problems.")
        if len(set(problem_ids)) != len(problem_ids):
            raise ValueError("A problem cannot appear twice in the same set.")
        for problem_id in problem_ids:
            self.get_problem(problem_id)
        self.practice_sets[set_id] = list(problem_ids)

    def create_session(self, session):
        session_id = f"s{len(self.sessions) + 1}"
        self.sessions[session_id] = deepcopy(session)
        return session_id

    def get_session(self, session_id):
        return deepcopy(self.sessions[session_id])

    def save_session(self, session_id, session):
        self.sessions[session_id] = deepcopy(session)

    def add_attempt(self, attempt):
        record = deepcopy(attempt)
        record["attempt_id"] = len(self.attempts) + 1
        self.attempts.append(record)

    def get_attempts(self, session_id):
        return deepcopy([a for a in self.attempts if a["session_id"] == session_id])

    def save_result(self, session_id, result):
        self.results[session_id] = deepcopy(result)

    def get_result(self, session_id):
        return deepcopy(self.results[session_id])
