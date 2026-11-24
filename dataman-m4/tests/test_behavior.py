import unittest
from dataman.logic import AnswerChecker
from dataman.store import MemoryStore


class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.checker = AnswerChecker(self.store)
        self.sid = self.checker.start_session("learner-1", "demo-set")

    def test_correct_first_try_finishes(self):
        result = self.checker.submit_answer(self.sid, 56)
        self.assertTrue(result["correct"])
        self.assertFalse(result["retry_allowed"])
        self.assertEqual(self.checker.get_summary(self.sid)["solved"], 1)

    def test_two_misses_preserve_history_and_reveal_only_after_second(self):
        self.assertNotIn("answer", self.checker.get_state(self.sid))
        first = self.checker.submit_answer(self.sid, 50)
        self.assertTrue(first["retry_allowed"])
        self.assertNotIn("answer", first)
        self.assertEqual(self.checker.get_state(self.sid)["try_number"], 2)
        second = self.checker.submit_answer(self.sid, 54)
        self.assertFalse(second["retry_allowed"])
        self.assertEqual(second["answer"], 56)
        attempts = self.store.get_attempts(self.sid)
        self.assertEqual([a["submitted_answer"] for a in attempts], [50, 54])
        self.assertEqual([a["try_number"] for a in attempts], [1, 2])
        with self.assertRaises(ValueError):
            self.checker.submit_answer(self.sid, 56)
        self.assertEqual(len(self.store.get_attempts(self.sid)), 2)

    def test_correct_second_try(self):
        self.checker.submit_answer(self.sid, 50)
        result = self.checker.submit_answer(self.sid, 56)
        self.assertTrue(result["correct"])
        self.assertEqual(self.checker.get_summary(self.sid)["attempts"], 2)

    def test_invalid_input_does_not_consume_attempt(self):
        with self.assertRaises(ValueError):
            self.checker.submit_answer(self.sid, "abc")
        self.assertEqual(self.checker.get_state(self.sid)["try_number"], 1)
        self.assertEqual(self.store.get_attempts(self.sid), [])

    def test_eleventh_problem_rejected_without_changing_set(self):
        for n in range(2, 12):
            pid = f"p{n}"
            self.store.problems[pid] = {"problem_id": pid, "prompt": "1 + 1 = ?", "answer": 2}
        for n in range(2, 11):
            self.checker.add_problem_to_set("demo-set", f"p{n}")
        before = self.store.get_set("demo-set")
        with self.assertRaises(ValueError):
            self.checker.add_problem_to_set("demo-set", "p11")
        self.assertEqual(self.store.get_set("demo-set"), before)
        with self.assertRaises(ValueError):
            self.store.save_set("oversized", before + ["p11"])

    def test_recreated_service_shares_state_but_new_store_loses_it(self):
        self.checker.submit_answer(self.sid, 50)
        replacement = AnswerChecker(self.store)
        self.assertEqual(replacement.get_state(self.sid)["try_number"], 2)
        with self.assertRaises(KeyError):
            AnswerChecker(MemoryStore()).get_state(self.sid)


if __name__ == "__main__":
    unittest.main()
