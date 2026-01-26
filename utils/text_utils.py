import difflib

def calculate_similarity(target, actual):
    matcher = difflib.SequenceMatcher(None, target.lower().split(), actual.lower().split())
    ratio = matcher.ratio()

    html_diff = []

    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        target_segment = target.split()[a0:a1]
        actual_segment = actual.split()[b0:b1]

        if opcode == 'equal':
            html_diff.append(f"<span class='correct'>{' '.join(target_segment)}</span>")
        elif opcode == 'insert':
            html_diff.append(f"<span class='wrong'>{' '.join(actual_segment)}</span>")
        elif opcode == 'delete':
            html_diff.append(f"<span class='missing'>[{' '.join(target_segment)}]</span>")
        elif opcode == 'replace':
            html_diff.append(
                f"<span class='wrong'>{' '.join(actual_segment)}</span> "
                f"<span class='missing'>({' '.join(target_segment)})</span>"
            )

    return ratio * 100, " ".join(html_diff)

