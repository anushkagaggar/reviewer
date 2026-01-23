def format_memory(stm, ltm):
    """
    Convert raw memory into reviewer instructions
    """

    lines = []

    # STM summary
    if stm:
        recent = stm[-1]

        issues = recent.get("key_issues", [])

        if issues:
            lines.append("Recent unresolved issues:")
            for issue in issues:
                lines.append(f"- {issue}")

    # LTM summary
    if ltm and ltm.get("recurring_issues"):
        lines.append("\nRecurring long-term issues:")

        for issue in ltm["recurring_issues"]:
            lines.append(f"- {issue}")

    if not lines:
        return "No prior review history available."

    return "\n".join(lines)
