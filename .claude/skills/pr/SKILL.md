---
name: pr
description: 現在のfeatureブランチをpushして、PRを作る（マージはしない）
disable-model-invocation: true
argument-hint: "[PRタイトル（省略可）]"
allowed-tools: Bash(git push -u origin *) Bash(gh pr create *) Bash(git branch *) Bash(git status *) Bash(git log *) Bash(git diff *)
---

# /pr：現在のブランチをpushして、PRを作る

引数：$ARGUMENTS（PRのタイトル。省略されたら、差分から日本語で付ける）

## 手順
1. `git branch --show-current` でブランチを確認する。main か master なら、何もpushせずに止まって、報告する。
2. `git status --short` で、未コミットの変更を確認する。あれば、止まって、報告する（勝手にコミットしない）。
3. `git log --oneline main..HEAD` と `git diff --stat main...HEAD` で、変更の内容を把握する。
4. PRのタイトルと本文を作る（下の雛形）。
5. `git push -u origin <ブランチ名>` を実行する。
6. `gh pr create --base main --title "<タイトル>" --body "<本文>"` を実行する。
7. PRのURLを表示して、終わる。マージは、しない。

## PRのタイトル
- 引数があれば、そのまま使う。なければ、コミットの内容から、短く付ける（例：`feat: ○○を追加`、`docs: ○○を直す`）。

## PRの本文（雛形）
```
理由：1〜2行（なぜ、この変更が必要か）

確認してほしい点
- 差分を読むときに、特に見てほしい所を、1〜2個
```

## 守ること
- 署名の行（Co-Authored-By、Generated with など）は、付けない。
- 公式で確認できていないことは、「未確認」と書く。
- mainへのpush、force push、PRのマージは、してはいけない。
