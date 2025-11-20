# AI News Aggregator

AI関連のニュースを収集し、LLMを用いて3行で要約して表示するWebアプリケーションです。

## 機能

- **ニュース収集**: AI関連のニュースをクローリング（現在はモックデータを使用）。
- **AI要約**: 記事の内容を3行に要約（現在はモックLLMサービスを使用）。
- **カード表示**: 白を基調とした見やすいカードデザインで記事を表示。
- **いいね機能**: 各記事に対して「いいね」ができ、カウントが保存されます。

## 技術スタック

- **Frontend**: React, TypeScript, Vite, Vanilla CSS
- **Backend**: FastAPI, Python
- **Database**: In-memory (簡易実装)

## セットアップと実行方法

### 前提条件

- Node.js (v18以上推奨)
- Python (v3.8以上推奨)

### バックエンド (Backend)

1. ディレクトリに移動:
   ```bash
   cd backend
   ```
2. 仮想環境の作成と有効化:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Mac/Linux
   # python3 -m venv venv
   # source venv/bin/activate
   ```
3. 依存関係のインストール:
   ```bash
   pip install fastapi uvicorn
   ```
4. サーバーの起動:
   ```bash
   uvicorn main:app --reload
   ```
   サーバーは `http://localhost:8000` で起動します。

### フロントエンド (Frontend)

1. ディレクトリに移動:
   ```bash
   cd frontend
   ```
2. 依存関係のインストール:
   ```bash
   npm install
   ```
3. 開発サーバーの起動:
   ```bash
   npm run dev
   ```
   ブラウザで `http://localhost:5173` にアクセスしてください。

## 構成

- `backend/`: FastAPIバックエンドコード
- `frontend/`: Reactフロントエンドコード
