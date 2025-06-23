# AniClubSuperStir-Muddler

アニクライベントの告知ツイートを簡単に作成し、複数ツイートに分割して投稿を支援するWebアプリケーションです。

## 目次
- [AniClubSuperStir-Muddler](#aniclubsuperstir-muddler)
  - [目次](#目次)
  - [必要条件](#必要条件)
  - [セットアップ](#セットアップ)
  - [実行方法](#実行方法)
  - [使用技術](#使用技術)
  - [プロジェクト構成 (主要部分)](#プロジェクト構成-主要部分)

## 必要条件
- Python 3.9 以降
- pip (Pythonパッケージインストーラー)

## セットアップ
1. このリポジトリをクローンします:
   ```bash
   git clone https://github.com/your-username/AniClubSuperStir-Muddler.git
   cd AniClubSuperStir-Muddler
   ```
2. (推奨) 仮想環境を作成し、有効化します:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux の場合
   # venv\Scripts\activate    # Windows の場合
   ```
3. 必要な依存関係をインストールします:
   ```bash
   pip install -r requirements.txt
   ```

## 実行方法
開発サーバーを起動するには、ディレクトリ直下で以下のコマンドを実行してください:****
```bash
% uvicorn main:app --reload
```
起動後、ウェブブラウザで `http://127.0.0.1:8000` にアクセスしてください。

## 使用技術
- FastAPI
- Uvicorn
- Jinja2
- Pydantic
- Tailwind CSS
- DaisyUI

## プロジェクト構成 (主要部分)
```
AniClubSuperStir-Muddler/
├── app/                # FastAPIアプリケーションのメインコード
│   ├── main.py         # FastAPIアプリケーションインスタンスとグローバルルート
│   ├── models/         # Pydanticモデル (データ構造定義)
│   ├── routers/        # APIルーター (各エンドポイントの処理)
│   ├── services/       # ビジネスロジック (例: ツイート分割処理)
│   └── templates/      # Jinja2 HTMLテンプレート
├── requirements.txt    # Pythonの依存パッケージリスト 
└── README.md           # このファイル
```