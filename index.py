import os
import openai
import configs
import tiktoken

openai.organization = configs.OPENAI_ORG_ID
openai.api_key = configs.OPENAI_API_KEY

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
q1 = '''
Golangのコードレビューの[指摘リスト]指摘点を分類してもらえますか。指摘点は１行につき１つあります
[指摘点分類のイメージ]に合わせて細分化してください。
出力時は、[指摘リスト]全ての指摘点に対して指摘点分類を出力してください。
また、[出力イメージ]のように、[指摘リスト]の１つ指摘点の横にカンマで区切って指摘点分類を付け足して、１つの指摘点ごとに改行で区切って出力してください。

---
[出力イメージ]

No1,指摘点分類1,指摘点分類2
No2,指摘点分類1
...

---
[指摘点分類のイメージ]

・API定義誤り
  - 例
    - API定義、requiredの設定誤っている
・仕様確認
  - 例
    - ...
    - ...
・不要な処理
  - 例
    - ...
    - ...
・処理不足・考慮漏れ
  - 例
    - ...
    - ...
    - メールアドレス大文字・小文字問題について Cognito上にユーザが登録され、かつエラーになる場合がある
・排他制御
  - 例
    - 画面操作で担当者が0名になるのはNGです排他制御お願いします
・他機能の横展開
  - 例
    - ...
・実装誤り
  - 例
    - すべて空文字列（あるいは空の配列）の場合も、入力データが一つも存在しない扱い
・競合・マージ解決
  - 例
    - 競合してます解消してください
---
[指摘リスト]
No1.⚪︎⚪︎⚪︎
No2.⚪︎x△
...
'''

# you can try shortening your input 
print(num_tokens_from_string(q1,"cl100k_base"))

# create a chat completion
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {
            "role": "user",
            "content": q1
        },
    ],
    temperature=0,
    stream=True,
    # adjusting the max_tokens parameter to control the length of the generated output. Keep in mind that very long conversations might result in incomplete replies.
#    max_tokens = 4096,
)

for chunk in chat_completion:
    if len(chunk.choices) != 0:
        if chunk.choices[0].finish_reason == None:
            print(chunk.choices[0].delta.content,end='')
        else:
            break
