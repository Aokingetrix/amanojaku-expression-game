# 操作ガイド

## セットアップ

必要なものは64bit版Python 3.11とWebカメラです。Windows 10/11、x86_64 Linuxを対象にしています。
WindowsではMicrosoft Visual C++ Redistributable 2015–2022もインストールしてください。

uvを使う場合は[READMEの起動手順](../README.md#起動)を参照してください。pipを使う場合は、リポジトリのルートで次を実行します。

Windows PowerShell：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r deepface_ver\requirements.txt
.\.venv\Scripts\python.exe -m deepface_ver.scripts.main
```

Linux：

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r deepface_ver/requirements.txt
.venv/bin/python -m deepface_ver.scripts.main
```

初回の表情認識では、インターネット経由でモデルを取得します。読み込みが完了するまで少し待ってください。

## ゲームの流れと操作

タイトルで`S`を押し、説明を見るか選びます。`E`で説明をスキップできます。
名前を決めると3秒のカウントダウン後にゲームが始まります。

画面のキャラクターとは異なる表情を作ってください。キャラクターが複数いるときは、どのキャラクターとも違う表情を作ります。無表情と顔が映っていない場合も失敗になります。

| 場面 | 操作 |
| --- | --- |
| スタート・説明を進める・次のラウンド | `S` |
| 説明をスキップ | 説明の選択画面で`E` |
| 名前の履歴を選ぶ | `↑`・`↓` |
| 名前の履歴選択と文字入力を切り替える | `←`・`→` |
| 名前を確定する | `Enter` |
| 説明や名前選択から戻る | `Esc` |
| 終了画面からタイトルへ戻る | `R` |
| ゲームを終了する | `Shift+Esc`またはウィンドウの閉じるボタン |

プレイ中は次のラウンドまで進めるか、`Shift+Esc`で終了できます。

## カメラ・ウィンドウ設定

起動コマンドの末尾にオプションを付けられます。

```text
--camera-index N
--camera-backend auto|dshow|msmf|v4l2|default
--window-size WIDTHxHEIGHT
```

Windowsでカメラ番号とバックエンドを指定する例：

```powershell
.\.venv\Scripts\python.exe -m deepface_ver.scripts.main --camera-index 1 --camera-backend dshow
```

Linuxでウィンドウサイズを指定する例：

```bash
.venv/bin/python -m deepface_ver.scripts.main --window-size 1920x1080
```

バックエンドの既定値は`auto`です。WindowsではDirectShow→MSMF、LinuxではV4L2を優先して選びます。
画面はウィンドウに合わせてアスペクト比を保って拡大・縮小します。

## 困ったとき

| 状況 | 試すこと |
| --- | --- |
| カメラを開けない | カメラを使用中のアプリを閉じ、OSのカメラ権限を確認する |
| 別のカメラが映る | `--camera-index 0`や`--camera-index 1`で切り替える |
| Windowsで映像が取得できない | `--camera-backend dshow`または`--camera-backend msmf`を試す |
| 顔を認識しにくい | 顔を明るくし、カメラの正面を向く |
| 初回の認識が遅い | モデル取得と初期化の完了を待つ |

## ランキングの保存先

ランキングはテーマごとに保存されます。通常テーマのIDは`default`です。

- Windows：`%LOCALAPPDATA%\amanojaku-game\themes\<theme-id>\highscore.json`
- Linux：`${XDG_DATA_HOME:-~/.local/share}/amanojaku-game/themes/<theme-id>/highscore.json`

[READMEへ戻る](../README.md) / [テーマを変更する](development.md#テーマの変更)
