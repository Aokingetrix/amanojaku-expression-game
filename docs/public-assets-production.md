# 公開用素材の制作記録

制作日: 2026-10-31。

## キャラクター表情

OpenAIの組み込み画像生成ツール（imagegen）を使用。元素材の画像は入力していない。
この記録は再生成時の制作仕様であり、同じ画像が完全に再現されることを保証しない。

基本画像 `happy.png` のプロンプト:

> Use case: stylized-concept. Asset: one transparent PNG expression sprite for the original Japanese webcam game Amanojaku. Create a brand-new cute round amanojaku child demon face, two small cream horns, short midnight blue hair tuft, pale teal face, rounded navy outline, minimal flat clean shapes readable at 120 pixels. Happy expression: closed crescent eyes and clear broad smiling mouth, subtle rosy cheeks. Front-facing HEAD ONLY, no neck or body. Center in a square canvas with 12 percent empty transparent margin; full horns and face visible. One character, one expression, no text, no letters, no symbols, no watermark, no scenery. Do not imitate any existing character or artist. Actual transparent background.

残りの画像は上記の新規基本画像を参照し、以下のテンプレートに表情仕様を入れて生成する。

> Use case: precise-object-edit. Image 1 is the new original happy amanojaku sprite created for this game, the edit target. Produce one {key} expression sprite of exactly the same character. {expression} Change only eyes, eyebrows and mouth, and for sad add tears. Keep identical face shape, head size, hair, cream horns, ears, teal skin, navy outlines, coloring, head-only composition, square canvas and placement. Remove happy blush if inappropriate. Preserve genuine transparent background. No text, watermark, extra character, body or scenery.

| key | expression |
| --- | --- |
| sad | Sad and crying: raised inner eyebrows, eyes narrowed downward and small blue tears, clearly downturned mouth. |
| angry | Angry: eyebrows slant downward toward the center, narrowed eyes, small tightly frowning mouth. Mild cartoon frustration appropriate for a family game. |
| surprise | Surprised: raised eyebrows, wide round eyes with small pupils, clearly round open O mouth. |
| neutral | Neutral: relaxed horizontal eyebrows, simple open eyes, closed horizontal mouth, no smile, no frown and no tears. |

背景透過で生成し、PNGのアルファを保持する。保存先: `deepface_ver/data/public/emotions/`。
表情の内部キー・対応関係・ゲームルールは変更しない。

## アイコン・BGM

`tools/generate_public_assets.py` が作成する。

- アイコン: 時計・ハート・疑問符をPygameの幾何図形で描画した256×256 PNG。
- BGM: タイトル・プレイ・終了画面用の短い音高列。外部サンプルを使わず正弦波を合成。
- 音声形式: WAV、24,000 Hz、16-bit、mono。音の立ち上がりと末尾にフェードを付ける。
- タイトル100 BPM、プレイ120 BPM、終了90 BPM。各32個の8分音符。
- 保存先: `deepface_ver/data/public/icons/` と `deepface_ver/data/public/sounds/`。

生成物は確認用の初稿。画面での視認性と実際の音量・ループ感を実機で確認する。
元のMP3やイラストを編集・変換して新規素材と称することはしない。
