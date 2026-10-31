# 素材の出典と利用条件

確認日: 2026-10-31。コードのライセンスと、以下の素材固有の利用条件は別です。
この一覧は本リポジトリに同梱する現行テーマを対象にしています。

独自コード・独自文書・新規素材にはPolyForm Noncommercial License 1.0.0を適用します。
いらすとや、効果音ラボ、フォント、顔検出XML、外部ライブラリ・モデルは対象外です。
スクリーンショットに含まれる第三者素材も含め、元の権利者の利用条件を優先します。
詳細は[ライセンスと適用範囲](docs/licensing.md)を参照してください。

## 新しく作成するキャラクター表情

`deepface_ver/data/public/emotions/` のPNGは、このプロジェクト用にOpenAIの画像生成ツールで作成しています。
元の出典不明画像は参照入力に使っていません。同じキャラクターの表情違いには、今回新規生成した画像を参照しています。
制作プロンプトと生成方法は [制作記録](docs/public-assets-production.md) を参照してください。
AI生成画像であり、手描き作品や独自に学習したモデルの成果としては扱いません。

## プログラムで作成するアイコン・BGM

`deepface_ver/data/public/icons/*.png` と `deepface_ver/data/public/sounds/bgm_*.wav` は、
このプロジェクト用に追加した [生成スクリプト](tools/generate_public_assets.py) から作成します。
アイコンは幾何図形、BGMは記述した音高列と正弦波の合成です。外部画像・音源サンプル・既存曲を入力として使っていません。

```bash
python tools/generate_public_assets.py
```

## SE：効果音ラボ

対象:

- `deepface_ver/data/sounds/se_select.mp3`
- `deepface_ver/data/sounds/se_count.mp3`
- `deepface_ver/data/sounds/se_success.mp3`
- `deepface_ver/data/sounds/se_fail.mp3`

入手元は作者申告により [効果音ラボ「ボタン・システム音」](https://soundeffect-lab.info/sound/button/)。
元のダウンロード時の音源名とローカル名の対応は未確認です。

- [利用規約](https://soundeffect-lab.info/agreement/)
- [公式FAQ](https://soundeffect-lab.info/faq/)

公式FAQは、効果音を組み込んだアプリのGitHub公開と、音源ファイルが取り出せる状態での公開を認めています。
本ゲームの操作音・判定音として利用します。効果音集や素材配布を目的とする利用は行いません。
クレジットは任意ですが、出典を追えるよう記載しています。
著作権は効果音ラボに帰属し、本プロジェクトのPolyForm Noncommercialライセンスをこの音源へ適用しません。
音源単体の再配布・販売等は同サイトの規約に従ってください。

## 人間の表情イラスト：いらすとや

`deepface_ver/data/human_faces/*.png` 5枚は、制作者の申告によりいらすとや由来であり、本ゲームの表情対応表で使用します。
作者: みふねたかし。現在の同梱ファイルの加工・拡大経緯は未確認です。

- [公式サイト](https://www.irasutoya.com/)
- [利用規定](https://www.irasutoya.com/p/terms.html)
- [よくあるご質問](https://www.irasutoya.com/p/faq.html)

著作権は放棄されておらず、本プロジェクトのPolyForm Noncommercialライセンスを適用しません。
アプリ内利用と素材としての再配布には別の条件があります。
公式の関連素材ページは以下です。現在の加工済みファイルとの一対一の対応を証明したものではありません。

| 同梱ファイル | 関連する公式素材ページ | 確認状態 |
| --- | --- | --- |
| `happy_human.png`, `angry_human.png`, `sad_human.png` | [青年の表情](https://www.irasutoya.com/2012/06/blog-post_29.html) | 元画像との対応・加工経緯は要確認 |
| `surprise_human.png` | [女性の表情：驚いた顔等](https://www.irasutoya.com/2013/04/blog-post_5368.html) | 元画像との対応・加工経緯は要確認 |
| `no_exp_human.png` | [笑う女性（5段階）](https://www.irasutoya.com/2017/02/5_23.html) | 元画像との対応・加工経緯は要確認 |

一般的なアプリ内利用が認められていても、素材配布や独自のライセンスでの再許諾はしません。
元のダウンロードデータとの厳密な対応と加工経緯は未確認であり、追加で確認できた情報を本書へ反映します。
公式ページの存在だけを根拠に、現在の加工済みファイルが正規配布物と同一であるとは記載しません。

## フォント

`deepface_ver/data/fonts/NotoSansJP[wght].ttf` はNoto Sans JPです。
同梱の [SIL Open Font License 1.1](deepface_ver/data/fonts/OFL.txt) と
[フォントREADME](deepface_ver/data/fonts/README.md) を保持します。

## 顔検出用データ

`deepface_ver/data/cascades/haarcascade_frontalface_default.xml` はOpenCV由来のHaar Cascadeです。
XML冒頭のIntel License Agreement、著作権表記、再配布条件、免責事項を保持します。

## 同梱範囲

本リポジトリには、現行テーマの素材と顔写真を含まない画面プレビューを同梱しています。
実プレイ履歴や個人の顔が写った開発スクリーンショットは含めていません。
