## IB-Link 操作マニュアル（4.6-4.10）APIドキュメント修正 計画書

### 目的
- `docs/index.md` の **4.6〜4.10** は「開発者がDアプリ実装の参考にできる**既存実装例ベース**のユーザガイド」として利用される。
- 現状、**事実ベースではない内容（推測・一般論・マーケティング・未検証の仕様）が混入**しているため、**根拠が取れる情報だけ**に整理する。
- Dアプリ間でAPI利用に差異がある場合は、`docs/index.md` に **4.99** を新設し、**衝突・競合一覧**を集約して追えるようにする。

---

## スコープ

### 対象（修正対象）
- `docs/index.md` の以下セクション
  - 4.6 Chat API（L781〜）
  - 4.7 Documents API
  - 4.8 Retriever API
  - 4.9 Audio API
  - 4.10 モデル切り替え API（L1656〜）

### 参照元（事実根拠）
- **OpenAPI（一次仕様）**
  - `docs/api/openapi.ja.yaml`
  - `docs/api/openapi.en.yaml`
- **Dアプリの実装コード（一次根拠）**（※各Dアプリ内のMarkdownは読み飛ばし）
  - `manual/Dapp/d-josys/src`（最優先）
  - `manual/Dapp/d-sales/src`
  - `manual/Dapp/d-retail/src`
  - `manual/Dapp/d-medical/{assets,map_pointer,record_summary,report_maker,resource}`（ユーザー指定範囲）
- **Dアプリ実装の使用箇所マップ（本作業で作成済み）**
  - `manual/IBUGM/01_DAPP_API_USAGE_MAP.md`

---

## 現行 4.6〜4.10 の問題点（具体化）

### 4.6 Chat API（`docs/index.md` L781〜）
- **リクエストキーが不整合**
  - 例が `message`（単数）になっている（L796〜）一方、同ファイル内の別例（4.10内）では `messages`（複数）を使用（L1844〜）。
- **パス表記が不整合**
  - ベースURLが `http://localhost:8080/iblink/v1`（L786）かつエンドポイントが `/chat/completions`（L793）だが、4.10内の例は `http://localhost:8080/v1/chat/completions`（L1844〜）で整合しない。
- **HTTPステータスの根拠が不明**
  - レスポンス例が `202 Accepted` とされている（L816）が、OpenAPIにも定義がなく、実装根拠が現リポジトリ内に存在しないため断定できない。
- **参照リンクの妥当性はあるが、IB-Link固有の差分が未検証**
  - llama.cpp serverへのリンク（L824〜）は一般情報であり、IB-Linkのラッパー仕様（/iblink/v1の有無等）を保証しない。

#### 実装根拠から確定している事実（後工程で本文に残す/揃えるポイント）
- **OpenAI互換Chat（推論サーバ）**は、Dアプリ実装で `http://localhost:{port}/v1/chat/completions` を叩く（portはポリシーから決まる実装がある）。
- `messages`（system/user等の配列）を使用している実装が複数存在する。
- 起動直後に `503 Loading model` が返る前提で、`/v1/models` を使った到達性確認やリトライ分岐が実装されている（例: D-Josys / Retail / Medical）。

### 4.7 Documents API（`docs/index.md` L833〜）
- **フロー記述とOpenAPIが矛盾**
  - 「全ドキュメントを一覧表示（GET `/documents/list`）」（L844）と記載があるが、OpenAPIは `POST /documents/list`。
- **OpenAPIにない“周辺機能/統合サンプル/設定例”が混入**
  - `DocumentsAPIClient`（Python/Node）などのクライアントクラス（L1139〜）は本リポジトリに実装が存在せず、事実ベースでない可能性が高い。
  - `EmbeddingApi` の設定例（L1172〜）は、少なくともこのリポジトリのOpenAPI範囲外で、根拠が不足。
- **ベストプラクティス/最適化/セキュリティなどが“一般論”として混在**
  - 例: 「結果キャッシュ」等（L1196〜）は実装・運用で採用されているか未検証。

#### 実装根拠から確定している事実（後工程で本文に残す/揃えるポイント）
- D-Josys / Sales / Retail の実装で、`http://localhost:8500/iblink/v1/documents/{process,status,list,delete,search}` が利用されている。
- Dアプリ実装側で **`project_id` の正規化（例: `proj_default`→ゼロUUID）**や、`files` の整形（`{file_path, enable_ocr}`）を行っている箇所がある（= 本文はこの事実に沿わせる必要がある）。

### 4.8 Retriever API（`docs/index.md` L1214〜）
- **OpenAPI範囲外の依存説明が断定調**
  - “外部の埋め込みAPIを使用（デフォルト …）”（L1234）は、実装根拠がない限り断定できない。
- **エンドポイント表記の粒度が混在**
  - `/iblink/v1/retriever` のようにベースパス込みで書かれている箇所があり（L1228〜）、他APIの記載と一貫しない（統一が必要）。

#### 実装根拠から確定している事実（後工程で本文に残す/揃えるポイント）
- OpenAPI上は `http://localhost:6500/iblink/v1/retriever` が定義されている。
- Dアプリ実装の「通常コード」では Retriever を直接叩かないケースがある一方、Sales の検証/サンプル（`Tasks/cf/renderer.js`）に `POST {apiUrl}/iblink/v1/retriever` が存在する（= 本文では “利用例（既存実装）”として扱うか、4.99/補足へ寄せる判断が必要）。

### 4.9 Audio API（`docs/index.md` L1353〜）
- **OpenAPI未定義の機能が大量に含まれる**
  - WebSocket（`/v1/audio/stream`, `/v1/audio/realtime`）やプロトコル詳細（L1452〜）はOpenAPIに存在しないため、実装根拠が取れない限り削除候補。
- **性能/環境依存の主張が混入**
  - NPU 5〜10倍等（L1624〜）は再現条件が不明で、実装参考資料としてはノイズになりうる。
- **認証の断定**
  - `.env` の `API_KEY`（L1365）は実装根拠が必要（OpenAPI上は無認証）。

#### 実装根拠から確定している事実（後工程で本文に残す/揃えるポイント）
- Dアプリ実装では **WebSocket realtime**（例: `ws://127.0.0.1:8000/v1/audio/realtime`）を利用する実装が存在する（D-Josys / Sales / Retail / Medicalで観測）。
- 同時に、Dアプリ側には **音声“管理API”**（既定 `http://127.0.0.1:7100`）を前提にした `voiceManager` / `VoiceResourceManager` が存在する（= 8000のAudio APIとは別系統で、現行4.9の説明と混線しやすい）。
- Retailでは **Audio Hub / Realtime Hub**（例: `http://localhost:7000/realtime`, `http://localhost:7000/iblink/v1/audio/health`）も定数化されており、これも 8000/7100 と別系統。

### 4.10 モデル切り替え API（`docs/index.md` L1656〜）
- **マーケティング/設計思想の記述が中心で“実装参考”として過剰**
  - 「エンタープライズ向け」「本番運用で鍛えられた設計」等（L1660〜）は事実として検証が困難で、ガイドの目的（実装例）から逸脱。
- **実装がこのリポジトリに存在しない**
  - `src/IB-Link.LlamaServerAPI` を前提にしている（L1811〜）が、当該ソースが現リポジトリ内に存在しないため、仕様・起動手順・エンドポイント群を断定できない。
- **Chat APIとの整合性問題を内包**
  - 4.10内のcurl例は Chat API のURL/パス/リクエストキーと整合しない（L1844〜）。

#### 実装根拠から確定している事実（後工程で本文に残す/揃えるポイント）
- Dアプリ実装側には、**LlamaServerAPI（管理API）**として `http://localhost:9000/iblink/v1/llama-server/*` を叩く `LLMResourceManager` が存在する（D-Josys / Sales / Retail / Medicalで観測）。
- 役割は “推論サーバ（8080等）の起動/停止/状態取得/モデル一覧” であり、`docs/index.md` の 4.10 はこの実装事実に合わせて削ぎ落とす必要がある。

---

## あるべきアウトプット（MECEなAPIドキュメント）

各API（4.6〜4.10）は、以下の要素だけに限定する（＝根拠が取れる範囲のみ）。

- **Base URL**（環境変数/設定で変更可能なら、その事実と参照箇所）
- **Endpoints一覧**（メソッド＋パス。ベースパス込み/なしを統一）
- **Request**
  - Headers（必要なもののみ）
  - Query（必要なもののみ）
  - Body（JSONの実際のキー/型。OpenAPIまたは実装コードから引用）
- **Response**
  - 成功系（200/202等：実装またはOpenAPIの根拠がある場合のみ）
  - 失敗系（400/401/403/5xx：同上）
- **既存実装例（最重要）**
  - Dアプリの実コードに存在する例のみ
  - 例は「呼び出し最小構成」と「実運用で使っている構成」を分ける
- **制約**
  - タイムアウト、ストリーミング方式、ファイルパス制約、OS依存など、実装に現れているもののみ

削除対象（原則）
- 一般的ベストプラクティス、推奨、性能主張、未検証の将来機能、外部記事の内容の焼き直し

---

## Dアプリ実装の検証手順（Markdownは除外）

### 0) 参照順（固定）
- **D-Josys → Sales → Retail → Medical**（ユーザー指定の優先順）
- 参照は `manual/IBUGM/01_DAPP_API_USAGE_MAP.md` を入口とし、そこから各アプリの一次ソース（JS/HTML/Preload/Main）へ降りる。

### 1) 抽出する観点（APIごと）
- **URL/ポート**: `localhost:8080/8500/6500/8000/9000` 等
- **パス**: `/chat/completions`, `/documents/*`, `/retriever*`, `/v1/audio/*`, `/iblink/v1/llama-server/*`
- **Headers**: `Content-Type`, 認証ヘッダ（存在すれば）
- **Bodyキー/互換処理**: `message` vs `messages`、`text`→`query` などの吸収ロジック有無
- **ストリーミング**: `stream:true` の場合の形式（SSE/WS）とパース実装（`data: {json}` / `[DONE]` 等）
- **エラーハンドリング**: リトライ有無、例外/エラー表示、ユーザ通知

### 2) 収集物（計画）
- APIごとに「実装から観測された仕様」を `01_DAPP_API_USAGE_MAP.md` に追記し、`docs/index.md` 側に反映する際の“出典”にする。
- OpenAPIのあるAPI（Documents/Retriever/Audio HTTP）は、OpenAPIとの差分を列挙する（差分は4.99の候補にもなる）。

---

## APIドキュメント種別はMECEか？（分類の再点検）

### 現行（4.6〜4.10）の分類
- Chat / Documents / Retriever / Audio / モデル切り替え

### 実装で観測された追加カテゴリ候補（※4.6〜4.10の範囲外として扱うか要検討）
- **Voice 管理API（7100）**: `http://127.0.0.1:7100`（音声サーバ管理・起動停止等）
- **Audio Hub / Realtime Hub（7000）**: `http://localhost:7000/realtime` 等（Retail側で定数化）
- **Foundry Local API（9500）**: `http://localhost:9500/iblink/v1/foundry-local`（LLM系の別バックエンド）

> 上記は「4.6〜4.10を削ぎ落として事実化する」作業の中で、4.99（競合一覧）または別章（将来）として切り出す判断を行う。

---

## 4.99 競合（衝突）一覧の設計（`docs/index.md` に追加予定）

### 4.99 の目的
- Dアプリ間で同一APIの使い方が異なる場合、本文に散らさず **一箇所で差分を追跡**する。

### 4.99 の最低フォーマット（案）
- **CONFLICT-YYYYMMDD-XX**
  - **対象API**: Chat / Documents / Retriever / Audio / ModelSwitch
  - **衝突点**: 1行で（例: “Chat APIのmessagesキーがアプリ間で不一致”）
  - **D-Josys（事実）**:
  - **Sales（事実）**:
  - **Retail（事実）**:
  - **Medical（事実）**:
  - **解決状況**: 未決 / 決定済（決定は後工程）
  - **根拠**: 各アプリの該当ファイルパス＋行範囲

### 4.99 に起票する代表的な衝突点（実装観測ベースの候補）
- **Chat API の baseUrl/ポート解決**: 固定8080 vs ポリシーport追従（`dapp_llm_base_url`/`llmManager.getPolicy` 等）
- **Chat API のストリーミング方式**: `stream:true` のSSE実装有無（Retailの Product Assistant 等）
- **Documents API の必須パラメータ**: `d_app_id`/`project_id` を必須とするクライアント実装 vs Main側フォールバックで省略されるケース
- **Audio API の系統分離**: 8000（WS realtime/HTTP health/status）と 7100（管理API）と 7000（Hub）の混同
- **モデル切替（LlamaServerAPI）**: server_config/custom_arguments の持ち方（辞書/文字列）と appsettings 参照有無

---

## 実作業の進め方（この計画書の次工程／※今は実施しない）

1. `docs/index.md`（4.6〜4.10）を「事実/非事実」に仕分けし、非事実は削除候補としてマーキングする（編集は後工程）。
2. `manual/IBUGM/01_DAPP_API_USAGE_MAP.md` を一次根拠として、各APIの **Base URL / Path / Request / Response / streaming / error** を整理する。
3. OpenAPIがあるAPI（Documents/Retriever/Audio HTTP）は OpenAPI を一次仕様として本文を同期し、Dアプリ実装は「利用例」として添える。
4. OpenAPIがない/不足する領域（Chatの実際の使い方、LlamaServerAPI管理、Audio WS realtime、Voice管理API等）は **Dアプリ実装例＝一次根拠**として記述し、未検証事項は書かない。
5. アプリ間差分は本文に散らさず 4.99 に集約する（根拠は必ずファイル/行で提示する）。

