# Web Security AI Analyzer

<img width="920" height="842" alt="画面イメージ" src="https://github.com/user-attachments/assets/ae93e8d1-c5fc-4376-a316-2466511be383" />
<img width="923" height="897" alt="画面イメージ2" src="https://github.com/user-attachments/assets/2ac7b7e0-87d5-4086-be38-62148272a099" />


このプロジェクトは、指定されたURLのセキュリティ状態をAI（Gemini 2.0 Flash）が診断し、その結果を視覚化するWebアプリケーションです。<br>
脆弱性の原因と想定される脅威を知ることができるので、セキュリティの学習にも役立ちます。

## 機能
- **セキュリティスキャン**: HTTPレスポンスヘッダーやHTML構造（フォーム、古いJS等）を解析。
- **AI診断**: セキュリティ専門家の知識を持つAIが、脆弱性と対策を提案。
- **データフロー視覚化**: ReactFlowを使用して、攻撃者が狙うデータパスを図解。

## 技術スタック
- **Frontend**: React, ReactFlow, Styled-components, Axios
- **Backend**: Flask, BeautifulSoup4, Google GenAI SDK (Gemini 2.0 Flash)

## セットアップ

### 1. バックエンド
1. `backend` ディレクトリへ移動
2. 仮想環境の作成と起動:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
3. ライブラリのインストール:
    `pip install -r requirements.txt`
4. .env ファイルを作成し、APIキーを設定:
    GOOGLE_API_KEY=あなたのGoogleAIStudioキー

### 2.フロントエンド
1. `frontend` ディレクトリへ移動
2. ライブラリのインストール
   npm install
3. アプリの起動
   npm start
