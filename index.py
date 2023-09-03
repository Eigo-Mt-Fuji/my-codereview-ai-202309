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
    - 対応可能部材種別に指定されたIDが、マスタ登録されている・いないの確認が 行われていない? 返却するメッセージIDの方針を認識合わせたいです
    - スペックイン対象が0件だった場合、処理をスキップすると書かれていますが、バリデーションエラーにする必要がないか確認したいです
・不要な処理
  - 例
    - 相談/依頼先ステータスを更新する処理は設計見積更新APIでも実施した方が良いか（なくても良いか）確認が必要
    - presenter/rest/design_project.go 705行目の分岐は 設計案件ID と 企業IDの比較をしているのは間違いなので修正が必要(不要な分岐であれば削除)
・処理不足・考慮漏れ
  - 例
    - パラメータの部材メーカーIDをもとに依頼先/部材メーカーID取得する処理が必要
    - 対応可能部材種別に指定されたIDが、マスタ登録されている・いないの確認が 行われていない? 返却するメッセージIDの方針を認識合わせたいです
    - メールアドレス大文字・小文字問題について Cognito上にユーザが登録され、かつエラーになる場合がある
・排他制御
  - 例
    - 担当者選択の画面操作で担当者が0名になるのは、業務上NGになりますので、排他制御をお願いいたします
・他機能の横展開
  - 例
    - 設計見積更新のPRの方でファイルの削除をトランザクションの外に移動いただいていた部分がこちらにも展開必要か に該当
・実装誤り
  - 例
    - s3Service.DeleteBusinessFileの呼び出しタイミングについて、更新失敗時に元のファイルが参照できなくなることを避けるために、 DBの削除クエリ実行より後に実施いただく必要があると思いました
    - すべて空文字列（あるいは空の配列）の場合も、入力データが一つも存在しない扱い
・競合・マージ解決
  - 例
    - mergeについてですが、現状は早送りmergeが必須というわけではないです。他のPRのmergeタイミングによっては延々とdevelopを取り込まないといけなくなる(+その都度承認作業が発生するので効率が悪い)可能性があるため推奨程度の温度感です。ただ必須ではないですが、PR出してからある程度時間が経過した場合はなるべく最新のdevelopを取り込んでからmergeしていただくようにしてほしいです
    - 競合してますので解消してください
---
[指摘リスト]
No1.部材メーカー側はproductMakerIDと自社の企業IDが一致する場合のみ許可するように修正必要
No2.パラメータの部材メーカーIDをもとに依頼先/部材メーカーID取得する処理が必要
No3.mergeについてですが、現状は早送りmergeが必須というわけではないです。他のPRのmergeタイミングによっては延々とdevelopを取り込まないといけなくなる(+その都度承認作業が発生するので効率が悪い)可能性があるため推奨程度の温度感です。ただ必須ではないですが、PR出してからある程度時間が経過した場合はなるべく最新のdevelopを取り込んでからmergeしていただくようにしてほしいです
No4.presenter/rest/design_project.go 705行目の分岐は 設計案件ID と 企業IDの比較をしているのは間違いなので修正が必要(不要な分岐であれば削除)
No5.「設計案件の企業IDとリクエストを送ったユーザーの企業IDが同一ではない」とバリデーション仕様ですが 認可サービスで行ってる「自社関連設計案件」のチェックと同じ（置き換えられた）理解であっていますか
No6.リスト取得する際、設計案件IDだけなく企業ID(corporationのid)も一致する 担当ユーザだけが取得対象になるように修正が必要に見えました。OpenAPI定義では 設計案件一覧APIのパスに「corporations/self」が含まれているためです
No7.修正いただいたことで、GetListByDesignProjectIDという関数が使われなくなってるように見えたのでもし不要な場合は削除いただきたいです
No8.機能設計書に記載されている「設計案件 相談先/依頼先のステータスを承諾済に更新」に該当する実装について、依頼先ステータスの更新処理が必要そうです。依頼先のロックをかけつつ更新されるイメージです
No9.s3Service.DeleteBusinessFileの呼び出しタイミングについて、更新失敗時に元のファイルが参照できなくなることを避けるために、 DBの削除クエリ実行より後に実施いただく必要があると思いました
No10.設計見積更新のPRの方でファイルの削除をトランザクションの外に移動いただいていた部分がこちらにも展開必要か
No11.設計見積更新時に使う案件通知種別について
No12.現在prjnotificationkind.RegisteredQuotationになっていますが、 機能設計書では「案件通知種別：updated_quotation」と記載されていました
No13.相談/依頼先ステータスを更新する処理は設計見積更新APIでも実施した方が良いか（なくても良いか）確認が必要
No14.機能設計書の設計見積更新シートには依頼先ステータス更新する処理は登場しないようです
No15.競合してますので解消してください
No16.設計案件依頼先のフィールドバグが修正されたので取り込みお願いします
No17.スペックイン更新（設計事務所）APIのデータ状態判定関数はスペックイン更新チェックのみの実行で問題ない
No18.API定義、requiredの設定誤っている
No19.すべて空文字列（あるいは空の配列）の場合も、入力データが一つも存在しない扱い
No20.指定した設計案件IDの設計案件ステータスが「クローズ」の場合 SE035は機能設計書の記載誤り
No21.担当ユーザ削除(#251)時は案件の担当者を0名とすることはできないという制御が正しい
No22.担当者選択の画面操作で担当者が0名になるのは、業務上NGになりますので、排他制御をお願いいたします
No23.更新することで管理者が0名になるケースについて
No29.設計案件ステータスをCloseに変更する必要はない理解であっていますか?（あっていれば該当する処理を削除されたいです）
No30.相談/依頼先ステータスに未回答が存在することの判定条件
No31.存在確認をする目的の場合の実装について(FYI)
No32.consultationProject, cooperationQuotationProject２つのbool型の変数名について
No33.見積金額(税込)の項目について、マイナスの許可不許可を念のため確認
No34.設定項目1-10の入力桁数制限の正しい仕様が、50と100のどちらか確認
No35.メールアドレス大文字小文字問題について Cognito上にユーザが登録され、かつエラーになる場合がある
No36.エラー時に メッセージID: ISE003を返却し、Fatalログ出力する必要があるか-> ない。ISE003の表示についてはフロント側で対応していただけることになった
No37.対応可能部材種別に指定されたIDが、マスタ登録されているいないの確認が 行われていない? 返却するメッセージIDの方針を認識合わせたいです
No38.domain/business/corp/corporation_test.goいくつかの関数についてテスト関数が存在しないように見えた( もし支障あれば追加 )
No39.添付ファイルをmoveではなくコピー後に削除処理するようにする
No40.添付ファイル関連のリクエストAPI定義とOrderについてフィールドについて
No41.設計案件ログに設計案件部材種別単位のログを判定できる方法を実装する
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
            print(chunk.choices[0].finish_reason)
            break
