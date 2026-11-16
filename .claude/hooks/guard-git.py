#!/usr/bin/env python3
"""Claude Code の PreToolUse フック：危険な git / gh コマンドを止める。

標準入力に JSON が届く（tool_input.command にコマンド文字列が入っている）。
終了コード 2 で、そのコマンドをブロックする（理由は標準エラー出力に書く）。
止めるもの：
  - gh pr merge（マージは作者が行う）
  - git push の force 系（--force, -f, --force-with-lease, +refspec）、--mirror、--delete
  - main / master ブランチからの git push、main / master を指す git push
"""
import json
import re
import shlex
import subprocess
import sys

PROTECTED = ("main", "master")
# 1つのコマンド文字列を、; && || | で区切る
SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\|")


def block(reason: str) -> None:
    print(f"ブロックしました：{reason}", file=sys.stderr)
    sys.exit(2)


def current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    return result.stdout.strip()


def git_subcommand(tokens: list[str]) -> tuple[str | None, list[str]]:
    """tokens[0] が git のとき、サブコマンド名と、その後ろの引数を返す。
    git -C <dir> push や git -c key=value push のようなオプションは読み飛ばす。"""
    i = 1
    while i < len(tokens):
        token = tokens[i]
        if token in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            i += 2
            continue
        if token.startswith("-"):
            i += 1
            continue
        return token, tokens[i + 1 :]
    return None, []


def check_push(args: list[str]) -> None:
    for arg in args:
        if arg in ("--force", "--force-with-lease", "-f", "--mirror", "--delete"):
            block(f"git push {arg}")
        if arg.startswith("--force-with-lease=") or (arg.startswith("+") and len(arg) > 1):
            block("force push")
    if current_branch() in PROTECTED:
        block("main ブランチからの git push")
    for arg in args:
        name = arg.split(":")[-1].removeprefix("refs/heads/")
        if name in PROTECTED:
            block("main を指す git push")


def check_segment(segment: str) -> None:
    tokens = shlex.split(segment)
    # FOO=bar git ... のような、環境変数の前置きを読み飛ばす
    while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return
    if tokens[0] == "gh" and tokens[1:3] == ["pr", "merge"]:
        block("gh pr merge（マージは作者が行う）")
    if tokens[0] == "git":
        subcommand, args = git_subcommand(tokens)
        if subcommand == "push":
            check_push(args)


def main() -> None:
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")
    for segment in SEGMENT_SPLIT.split(command):
        try:
            check_segment(segment)
        except ValueError:
            # 引用符が閉じていないなど、解析できない場合は、push / merge を含むときだけ止める
            if re.search(r"\bpush\b|\bpr\s+merge\b", segment):
                block("コマンドを解析できず、push / merge を含むため")
    sys.exit(0)


if __name__ == "__main__":
    main()
