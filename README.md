# なんちゃってレビュー指摘解析AI

## これは何?

- 過去のレビュー指摘取り込んで、都合よくざっくりAI分類するプログラム
- OpenAIが必要です。
- 分類したら置かれた環境でのプログラム実装に関する傾向がわかります(傾向に合わせて対策しましょう)
## 実行手順

- .envファイルを作成

```
$ cat <<EOF > ./.env
OPENAI_ORG_ID="***************************************"
OPENAI_API_KEY="***************************************"                                                                                     
EOF
```

- インストール

```
pip install -r requirements.txt
```

- 実行

```
python index.py
```

- 実行結果

```
No1,処理不足・考慮漏れ
No2,処理不足・考慮漏れ
No3,競合・マージ解決
No4,不要な処理
No5,仕様確認
No6,仕様確認
No7,不要な処理
No8,仕様確認
No9,実装誤り
No10,他機能の横展開
No11,仕様確認
No12,仕様確認
No13,不要な処理
No14,仕様確認
No15,競合・マージ解決
No16,不要な処理
No17,仕様確認
No18,API定義誤り
No19,実装誤り
No20,仕様確認
No21,排他制御
No22,排他制御
No23,仕様確認
No29,仕様確認
No30,仕様確認
No31,実装誤り
No32,実装誤り
No33,仕様確認
No34,仕様確認
No35,実装誤り
No36,仕様確認
No37,仕様確認
No38,不要な処理
No39,実装誤り
No40,仕様確認
No41,実装誤り
```

## 依存関係

- https://pypi.org/project/python-dotenv/
- https://platform.openai.com/docs/api-reference
- https://github.com/openai/openai-cookbook/
- https://platform.openai.com/docs/introduction

