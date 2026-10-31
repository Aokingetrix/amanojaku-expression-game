# あまのじゃくゲーム

[![Fast CI](https://github.com/Aokingetrix/amanojaku-expression-game/actions/workflows/ci.yml/badge.svg)](https://github.com/Aokingetrix/amanojaku-expression-game/actions/workflows/ci.yml)

Webカメラに向かって、画面のキャラクターと**違う表情**を作るゲームです。
Python・Pygame・OpenCV・DeepFaceを使い、表情認識とゲーム画面を組み合わせています。

![表情の対応関係画面](docs/images/emotion-map.png)

現行の描画処理からカメラなしで出力した画面です。実際のゲームではプレイ画面の右側にカメラ映像が表示されます。

## 制作背景・担当範囲

EEIC後期実験の授業課題として個人制作し、授業での制作後、文化祭でも公開しました。
企画、ゲームルール、UI、カメラ・表情認識の組み込み、素材の選定、テスト・動作確認など、制作全体を担当しています。

制作にはGeminiとCodexを全面的に使用し、生成AIの支援を受けながら実装・修正・リファクタリング・テスト作成を進めています。
表情認識には既存のDeepFaceモデルを組み込み、独自のモデル学習は行っていません。

## 遊び方

1. `S`でスタートし、遊び方と表情の対応を確認します。
2. 名前を選択してカウントダウンを待ちます。
3. 制限時間内に、表示されたキャラクターと異なる表情を作ります。
4. 成功すると得点が増え、制限時間が短くなります。失敗するとライフが減り、3回の失敗で終了します。

認識する表情は「ニコニコ・シクシク・ムカムカ・ビックリ・シーン」の5種類です。
無表情と顔未検出は失敗となります。得点に応じて同時に表示されるキャラクターが増えます。

| 操作 | キー |
| --- | --- |
| 決定・次のラウンド | `S` |
| 説明をスキップ | 選択画面で `E` |
| 戻る | `Esc`（プレイ中は無効） |
| 終了 | `Shift+Esc` またはウィンドウの閉じるボタン |
| 終了画面からタイトルへ | `R` |

## 実装のポイント

- **表情認識を別スレッドへ分離。** 推論中も画面更新を続け、処理待ちフレームは最新1枚だけ保持します。
- **状態と判定をテスト可能に。** `GameManager`は入力コマンドを受け取り、時計・乱数・音声を差し替えて状態遷移や得点を検証できます。
- **描画負荷を削減。** フォント、画像デコード、拡大画像をキャッシュし、起動時に素材を読み込みます。描画上限は30 FPSです。
- **Windows/Linuxの差異を吸収。** カメラのバックエンド、日本語フォント、スコア保存先を共通コードから選択します。
- **ゲームルールと素材を分離。** `theme.toml`で画像・背景・音声・表示文を変更できます。

[設計と処理の流れ](docs/architecture.md) / [性能の確認方法](docs/performance.md)

## 起動

必要環境は64bit版Python 3.11、Webカメラ、Windows 10/11 x64またはx86_64 Linuxです。
TensorFlowはCPUで実行します。WindowsではMicrosoft Visual C++ Redistributable 2015–2022も必要です。
コマンドはリポジトリのルートで実行してください。

```bash
git clone https://github.com/Aokingetrix/amanojaku-expression-game.git
cd amanojaku-expression-game
```

### uvを使う場合

[uvのインストール方法](https://docs.astral.sh/uv/getting-started/installation/)を参照してください。
Pythonのバージョンを指定して仮想環境を作成し、固定バージョンの依存関係を入れます。

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv -r deepface_ver/requirements.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m deepface_ver.scripts.main
```

Linux:

```bash
.venv/bin/python -m deepface_ver.scripts.main
```

仮想環境の有効化は必須ではありません。既存の`.venv`がある場合は、そのPythonが3.11であることを確認してください。
pipを使う手順、カメラ番号・バックエンド指定、外部テーマの詳細は[実行ガイド](deepface_ver/README.md)にあります。

初回の表情認識ではモデル取得・TensorFlowの初期化に時間がかかります。モデル取得にはインターネット接続が必要です。

## 構成

```text
deepface_ver/
  application.py   # 初期化、イベント処理、画面更新、終了処理
  core/            # 状態機械、保存、カメラ選択、テーマ、素材キャッシュ
  emo/             # OpenCVのカメラ取得とDeepFace認識ワーカー
  ui/              # 画面別描画、名前選択、UI部品
  scripts/main.py  # CLIエントリーポイント
  data/            # テーマと同梱素材、空のスコア初期値
  tests/           # ゲームルール、保存、テーマ、描画等のテスト
tools/             # 素材生成とカメラなしの画面プレビュー
```

## 開発・テスト

TensorFlowを入れずにゲーム状態・保存・テーマ・描画を確認する高速テスト:

```bash
uv pip install --python .venv -r requirements-dev.txt pygame==2.6.1
```

以降の`python`は仮想環境のPythonを使います。Windowsでは`.\.venv\Scripts\python.exe`、Linuxでは`.venv/bin/python`に置き換えられます。

```bash
python -m pytest
python -m ruff check deepface_ver/application.py deepface_ver/core deepface_ver/scripts deepface_ver/tests deepface_ver/ui tools
python -m ruff format --check deepface_ver/application.py deepface_ver/core deepface_ver/scripts deepface_ver/tests deepface_ver/ui tools
```

[Fast CI](.github/workflows/ci.yml)はUbuntuとWindows、Python 3.11で実行します。
[Full Runtime Smoke](.github/workflows/full-runtime.yml)はTensorFlow・DeepFaceを含む依存関係のインストールとインポートを確認します。
カメラ・実推論・音声出力の実機試験はCIとは別です。

## 保存データ・制約

- スコアはWindowsでは`%LOCALAPPDATA%/amanojaku-game/`、Linuxでは`$XDG_DATA_HOME/amanojaku-game/`（未設定なら`~/.local/share/amanojaku-game/`）へ保存します。
- アプリのコードにはカメラ映像を録画・保存・アップロードする処理を実装していません。依存ライブラリによる初回モデル取得は別途発生します。
- 表情分類には誤認識があり、照明・顔の向き等に影響されます。人の心理状態を判定する用途を想定していません。
- Windowsでは旧素材版で一通りのプレイを確認済みです。新素材の見た目・音量と、現行版のLinuxカメラ実機確認は継続中です。

## 制作と素材

実装・リファクタリング・テスト作成に生成AIを利用しています。表情認識は既存のDeepFaceモデルを使用し、独自のモデル学習は行っていません。
キャラクター表情は新規AI生成、アイコンとBGMは生成スクリプトで作成しています。人間イラストはいらすとや、SEは効果音ラボの素材です。

[素材出典・利用条件](ATTRIBUTIONS.md) / [新規素材の制作記録](docs/public-assets-production.md)

## ライセンス

本プロジェクト独自のコード・文書・新規素材は、[PolyForm Noncommercial License 1.0.0](LICENSE)で提供します。
ライセンスで定める非商用目的の利用・改変・再配布を認めます。商用利用を一般に許諾するものではありません。
商用利用の制限があるため、オープンソースではなく「非商用ライセンスでソース公開」として扱います。

いらすとや、効果音ラボ、フォント、顔検出データ、依存ライブラリ・モデルは対象外です。
文書や画面プレビューに含まれる第三者素材にも、それぞれの利用条件が適用されます。
詳しくは[適用範囲](docs/licensing.md)と[素材出典](ATTRIBUTIONS.md)を参照してください。
