"""問題のデータについての、決まりごと（1か所に、まとめる）。

選択肢の数を変えたくなったとき（例：5択）は、OPTION_COUNT を変えるだけにする。
"""

OPTION_COUNT = 4   # 1問あたりの選択肢の数（4択）
CORRECT_COUNT = 1  # 1問あたりの正解の数


def validate_choices(is_correct_flags: list[bool]) -> None:
    """選択肢の数と、正解の数が、決まりどおりか確認する。おかしければ ValueError を出す。"""
    if len(is_correct_flags) != OPTION_COUNT:
        raise ValueError(
            f"選択肢は {OPTION_COUNT} 個必要です（{len(is_correct_flags)} 個ありました）"
        )
    correct = sum(is_correct_flags)
    if correct != CORRECT_COUNT:
        raise ValueError(f"正解は {CORRECT_COUNT} 個必要です（{correct} 個ありました）")
