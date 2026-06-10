# Streamlit Community Cloud デプロイ手順

## 前提

- GitHub アカウント
- [GitHub CLI](https://cli.github.com/)（`gh`）推奨

## クイックデプロイ（推奨）

```bash
cd ~/Desktop/card-compare
./scripts/deploy.sh
```

初回はブラウザで GitHub ログイン（デバイス認証）が求められます。  
push 完了後、表示される手順に従い [share.streamlit.io](https://share.streamlit.io) でアプリを作成してください。

リポジトリ名を変える場合:

```bash
./scripts/deploy.sh my-card-compare
```

## 手動デプロイ

### 1. GitHub へ push

```bash
cd ~/Desktop/card-compare
git remote add origin https://github.com/<your-username>/card-compare.git
git push -u origin main
```

### 2. Streamlit Community Cloud でデプロイ

1. [share.streamlit.io](https://share.streamlit.io) にアクセス
2. GitHub アカウントでログイン
3. **Create app** をクリック
4. 設定:
   - **Repository**: `<your-username>/card-compare`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **Deploy** をクリック

数分後、`https://<app-name>-<hash>.streamlit.app` で公開されます。

### 3. カスタムサブドメイン（任意）

Streamlit Cloud のアプリ設定から App URL を変更できます（例: `card-compare.streamlit.app`）。

### 4. 再デプロイ

`main` ブランチへの push で自動的に再デプロイされます。

## ローカル確認

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 注意事項

- `.env` や `secrets.toml` に機密情報を含めない（Phase 1 では Secrets 不要）
- `requirements.txt` に全依存関係を記載する
- Python 3.10 以上を推奨

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| ModuleNotFoundError: src | `app.py` がリポジトリルートにあることを確認 |
| デプロイ失敗 | Cloud のログで `requirements.txt` のエラーを確認 |
| 共有URLが localhost | 本番では Host ヘッダーが streamlit.app になるため自動で https になる |
