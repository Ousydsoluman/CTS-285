"""Text interface. Run with: python app.py"""
from dataman.logic import AnswerChecker
from dataman.store import MemoryStore


def main():
    checker = AnswerChecker(MemoryStore())
    print("DataMan - Check an Answer")
    print("Temporary demo: progress is lost when this program closes.")
    print("Enter q to quit.\n")
    session_id = checker.start_session("demo-learner", "demo-set")
    while True:
        state = checker.get_state(session_id)
        if state["finished"]:
            break
        print(state["prompt"])
        print(f"Try {state['try_number']} of 2")
        raw = input("Your answer: ").strip()
        if raw.lower() == "q":
            print("Leaving demo. This temporary session will not survive closing.")
            return
        try:
            answer = int(raw)
        except ValueError:
            print("Please enter a whole number. No attempt was used.\n")
            continue
        result = checker.submit_answer(session_id, answer)
        if result["correct"]:
            print("Correct!")
        elif result["retry_allowed"]:
            print("EEE - Not quite. Try again. One attempt remains.")
        else:
            print(f"EEE - No attempts remain. The correct answer is {result['answer']}.")
        print()
    summary = checker.get_summary(session_id)
    print(f"Session complete: {summary['solved']} of {summary['total']} problems solved.")
    print(f"Attempts recorded: {summary['attempts']}")


if __name__ == "__main__":
    main()
