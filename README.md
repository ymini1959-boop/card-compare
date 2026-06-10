# クレジットカード比較ツール（エポスプラチナ基準）

エポスプラチナカードを基準に、楽天・Amex・dカード・PayPay 周辺のカードを軸選択式で動的比較する Streamlit アプリです。

## ローカル実行

```bash
cd card-compare
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## テスト

```bash
pytest tests/
```

## デプロイ

Streamlit Community Cloud へのデプロイ手順は [docs/deploy.md](docs/deploy.md) を参照してください。

## 免責

本サイトは各カード会社の公式サイトではありません。試算結果は参考値です。
