# switch-bot

SwitchBotのAPIを発行し、デバイスを制御する。

## 事前準備

- python3

以下のファイルを作成する。

- token.txt: 取得したトークン文字列が格納されているテキストファイル
- secret.txt: 取得したシークレット文字列が格納されているテキストファイル

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

### 赤外線デバイス一覧

$ python3 switchbot.py get_infrared_devices

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

### 電力計からの値を取得

デバイス一覧を取得した時に、deviceTypeが"deviceType": "Plug Mini (JP)"デバイスが電力計。
get_statusコマンドを利用して、温湿度計のステータスを取得する。
- voltage: 電圧瞬時値 単位 [V]
- electricCurrent: 電流瞬時値、単位 [A]

### 赤外線デバイスの制御

$ python3 switchbot.py send_command --dev_id id [--action action] [--parameter param] [--type type]

`引数`
- dev_id: コマンドを送信するデバイスのID
- action: 送信するコマンド文字列(デフォルト 'turnOn')
- paramter: コマンドに付随するパラメータ(デフォルト 'default')
- type: コマンド種類(デフォルト 'command')

`戻り値`
JSON形式

### 複数の温湿度計からの値を取得

$ python3 meter.py

`戻り値`
JSON形式

## Bluetoothを利用

BLE Advertisementから計測値を取得する。
Bleakライブラリが必要

### 温湿度計から温度を取得

$ python3 meter_ble.py

`戻り値`
JSON形式

### プラグミニから電力を取得

$ pythoh3 plug_ble.py

`戻り値`
JSON形式

