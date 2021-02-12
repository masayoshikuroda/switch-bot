# switch-bot

SwitchBotのAPIを発行し、デバイスを制御する。

## 事前準備

- python3

以下のファイルを作成する。

- token.txt: 取得したトークン文字列が格納されているテキストファイル

## 利用方法

### デバイス一覧

$ python3 switchbot.py get_devices

`引数`
なし

`戻り値`
JOSN形式

フォーマットした方がわかりやすい。 例) ... | jq .
statuscodeが100であることを確認する。
ステータスを取得するデバイスIDを deviceIdの値から確認する。

### デバイスステータスの取得

$ python3 switchbot.py get_status --dev_id id

`引数`
- dev_id: ステータスを取得するデバイスのID

`戻り値`
JSON形式

フォーマットした方がわかりやすい。 例) ... | jq .
値のみ取得したい場合、jqコマンドを利用する。 例) ... | jq '.te.val'

### 温湿度計から値を取得

デバイス一覧を取得した時に、deviceTypeが "Meter"のデバイスが温湿度計。
get_statusコマンドを利用して、温湿度計のステータスを取得する。

### 赤外線デバイスの制御

TBD


