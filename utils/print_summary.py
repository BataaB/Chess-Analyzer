def print_summary(summary):
    print(f"OPENING: {summary["opening"]["name"]}")
    for color in ["white", "black"]:
        player = summary[color]["player"]
        result = summary[color]["result"]
        accuracy = summary[color]["accuracy_percent"]
        phase_accuracy = summary[color]["phase_accuracy"]

        print(f"\n{color.capitalize()} ({player}) — {result.upper()}")
        print(f"  Overall Accuracy: {accuracy}%")
        for phase, value in phase_accuracy.items():
            print(f"    {phase.capitalize()} Accuracy: {value}")
        for move, count in summary[color]["accuracy"].items():
            print(f"{move}: {count}")