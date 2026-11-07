# WebCraft

Web技術（HTTP・DB・認証など）の基礎を固めるための学習アプリ。自分で問題を作り、4択で解いて学ぶ。

目的は「動くもの」を作ることだけでなく、作る過程でWeb技術を学び、**自分で説明できる設計**にすること。

## 現在の状況（開発中）

| | 状態 |
|---|---|
| 仕様・設計（ER図、ADR） | 完了 |
| DBのモデル、マイグレーション | 完了（手元のDBに適用済み） |
| API（FastAPI） | 未着手 |
| 画面（React / TypeScript） | 未着手 |
| 認証、CI、デプロイ | 未着手（予定あり） |

予定は [docs/spec.md](docs/spec.md) の「スケジュール」を参照。

## 技術

- バックエンド：FastAPI（Python）
- DB：PostgreSQL 18.6（開発はDocker Compose）
- ORM / マイグレーション：SQLAlchemy 2.1、Alembic
- DBドライバ：psycopg（バージョン3）
- フロント：React / TypeScript（予定）

## ドキュメント

- [docs/spec.md](docs/spec.md)：仕様書とスケジュール
- [docs/er.md](docs/er.md)：ER図
- [docs/adr/](docs/adr/)：設計判断の記録（なぜそう決めたか）
- [docs/retro.md](docs/retro.md)：スプリントごとの振り返り
- [CLAUDE.md](CLAUDE.md)：AIアシスタントを使うときのルール（DB設計と認証は作者が先に案を書き、AIはレビューする、など）

## 開発環境の作り方

動作確認：Python 3.14.4、Docker Compose。

```bash
# 1. 設定ファイルを作る（.env は git に入れない）
cp .env.example .env
# .env を開いて、POSTGRES_PASSWORD を決める。
# DATABASE_URL の中のパスワードも、同じ値にそろえる。

# 2. DB（PostgreSQL）を起動する
docker compose up -d

# 3. Pythonの環境を作る
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. テーブルを作る（backend/ の中で実行する）
alembic upgrade head
```

手元のDBは、使い捨てとして扱う（データの保存先は指定していない）。作り直すときは、次を実行する。

```bash
docker compose down -v
docker compose up -d
cd backend && alembic upgrade head
```
