# 開発ガイド

[アーキテクチャ](architecture.md)に、処理の流れと主要ファイルをまとめています。

## テストと静的チェック

Python 3.11の仮想環境を用意し、開発用の依存関係をインストールします。

```bash
uv pip install --python .venv -r requirements-dev.txt pygame==2.6.1
```

以下の`python`には仮想環境のものを使ってください。Windowsは`.\.venv\Scripts\python.exe`、Linuxは`.venv/bin/python`です。

```bash
python -m pytest
python -m ruff check deepface_ver/application.py deepface_ver/core deepface_ver/scripts deepface_ver/tests deepface_ver/ui tools
python -m ruff format --check deepface_ver/application.py deepface_ver/core deepface_ver/scripts deepface_ver/tests deepface_ver/ui tools
```

状態遷移・得点・ライフ、ランキング保存、テーマの上書き、画像キャッシュ、画面描画、CLIを検査します。
DeepFace等がインストールされていない環境では、それらに依存するテストをスキップします。
認識ワーカーのテストは処理を差し替え、最新フレームの上書きと連続処理を確認します。

### CI

| ワークフロー | 内容 |
| --- | --- |
| [Fast CI](../.github/workflows/ci.yml) | Ubuntu／Windows、Python 3.11で軽量テスト・Ruff・画面プレビュー出力 |
| [Full Runtime Smoke](../.github/workflows/full-runtime.yml) | TensorFlow・DeepFace等の依存関係、インポート、CLI、全テスト |

テストの描画と音声処理にはSDL dummy driverを使います。カメラ・実モデルによる分類・スピーカー出力は実機で確認します。

## 画面プレビュー

```bash
python -m tools.render_preview
```

実際の描画関数を使い、タイトルと表情対応表を`docs/images/`へ出力します。

## 開発者画面

タイトルで`E`→`N`→`H`と順に押すと開発者画面へ移動し、`R`で戻ります。
表示FPS、フレーム時間、認識結果、顔検出状態、認識処理時間を確認できます。

遅延欄の値は、フレームの前処理から顔検出・表情分類までの1回分の処理時間です。
比較計測では、OS・CPU・カメラ・テーマ・測定時間をそろえ、モデル初期化後の値を記録します。

## テーマの変更

起動時に`--theme-dir`で、`theme.toml`を含むフォルダを指定します。

```bash
python -m deepface_ver.scripts.main --theme-dir deepface_ver/data/themes/test-shapes
```

環境変数`AMANOJAKU_THEME_DIR`でも指定でき、CLIオプションが優先されます。
次は、タイトルだけを上書きする最小の`theme.toml`です。

```toml
schema_version = 1
id = "my-theme"
display_name = "My Theme"

[text]
title = "My Expression Game"
```

| セクション | 変更対象 |
| --- | --- |
| `[text]` | タイトル・説明・表示ラベル |
| `[images]` | 表情・人物・アイコン |
| `[backgrounds]` | 画面別背景 |
| `[bgm]`・`[se]` | 音声 |

素材パスはマニフェストのあるフォルダからの相対パスです。未指定項目は同梱テーマを使い、指定したファイルが見つからない場合は起動時にエラーになります。

背景キーは`default`、`title`、`menu`、`instruction`、`emotion_map`、`name_select`、`countdown`、`gameplay`、`result`、`finish`です。
背景はcover、表情や人物画像はcontainで描画します。
全項目の例は[同梱テーマ](../deepface_ver/data/theme.toml)、読み込み処理は[theme.py](../deepface_ver/core/theme.py)を参照してください。

## アイコン・BGMの生成

```bash
python tools/generate_public_assets.py
```

幾何図形のアイコン3枚と、正弦波を合成したBGM3曲を`deepface_ver/data/public/`へ書き出します。
実行すると同フォルダ内のアイコン・BGMを上書きします。

[READMEへ戻る](../README.md) / [素材クレジット](../ATTRIBUTIONS.md)
