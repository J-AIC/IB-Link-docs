## APIドキュメント不足分（ギャップ）一覧 + 章立て案B（apidocs 1:1対応）

### 目的
- `docs/index.md` の 4.6〜4.10（Chat / Documents / Retriever / Audio / モデル切替）が、`docs/api/openapi.*.yaml`（一次仕様）と `manual/apidocs`（バックエンドUsage Examples）および Dアプリ実装境界と一致していないため、**不足しているドキュメント**と、**章タイトル/章数（案B）**を確定できる形で整理する。

---

## 命名ルール（重要）

### 公式名称を優先する
- `manual/apidocs/*.md` の先頭見出し（例: `# DocumentsAPI - Usage Examples`）に存在する名称は **公式名称**として扱う。

### 公式名称が存在しない場合は「名称未定」として扱う（勝手に命名しない）
- OpenAPI / `manual/apidocs` / Dアプリ実装内に **API名として明示されていない**ものは、章タイトルで “API名っぽく” 命名しない。
- その場合は **「名称未定（観測されるエンドポイント: ...）」**の形式で記載し、**第4章の後半（追加/補足）へ集約**する。

---

## 前提（一次仕様の範囲）

### `docs/api/openapi.(ja|en).yaml` の対象
- OpenAPI は **Documents / Retriever / Audio（8000系）**のみを統合した仕様。
- **LLM推論（/v1/chat/completions）・モデル管理（LlamaServer/FoundryLocal）・Embeddings（5000）・音声管理（7100）・Audio Hub（7000）**は OpenAPI の対象外。

根拠: `docs/api/openapi.ja.yaml` の `info.description` / `tags` / `paths`。

---

## `manual/apidocs` の現状（存在するUsage Examples）
- Documents: `manual/apidocs/DocumentsAPI_Usage_Examples.md`
- Retriever: `manual/apidocs/RetrieverAPI_Usage_Examples.md`
- Audio（IB-Link経由: 7000/iblink/v1/audio/*）: `manual/apidocs/AudioAPI_Usage_Examples.md`
- AudioNPU（Whisper Server + Realtime: 8000 + WS）: `manual/apidocs/AudioNPUAPI_Usage_Examples.md`
- Embeddings（5000/iblink/v1）: `manual/apidocs/EmbeddingsAPI_Usage_Examples.md`
- LlamaServer（9000/iblink/v1/llama-server）: `manual/apidocs/LlamaServerAPI_Usage_Examples.md`
- FoundryLocal（9500/iblink/v1/foundry-local）: `manual/apidocs/FoundryLocalAPI_Usage_Examples.md`

---

## Dアプリ実装における利用箇所一覧（案B：公式ドキュメントに対応する範囲）

> 方針: Dアプリの **実行コード（`.js` 等）**に限定して列挙する。Markdown/メモ類（`*.md`）は除外する。

### DocumentsAPI（`manual/apidocs/DocumentsAPI_Usage_Examples.md`）
- **D-Josys**
  - `manual/Dapp/d-josys/src/api/IBLinkClient.js`（`/documents/process|status|list|delete|search`）
  - `manual/Dapp/d-josys/src/assets/js/apiClient.js`（`POST {IBLINK_SEARCH_BASE_URL}/v1/documents/search`）
- **Sales**
  - `manual/Dapp/d-sales/src/api/IBLinkClient.js`（`/documents/process|status|list|delete|search`）
  - `manual/Dapp/d-sales/src/preload.js`（Documents処理のIPC公開：`window.iblinkProcessDocuments`）
- **Retail**
  - `manual/Dapp/d-retail/src/main.js`（Main側で `http://localhost:8500/iblink/v1/documents/{process,delete,search}` を中継）
- **Medical**
  - **未使用（実行コード上で `/documents/*` 呼び出しは未検出）**

### RetrieverAPI（`manual/apidocs/RetrieverAPI_Usage_Examples.md`）
- **D-Josys**
  - `manual/Dapp/d-josys/src/index.js`（`iblink:documentRetriever` は 501 を返す＝Retriever利用は無効化方針）
- **Sales**
  - `manual/Dapp/d-sales/src/Tasks/cf/renderer.js`（検証用：`POST {apiUrl}/iblink/v1/retriever`）
- **Retail**
  - **未使用（実行コード上で `/retriever` 呼び出しは未検出）**
- **Medical**
  - **未使用（実行コード上で `/retriever` 呼び出しは未検出）**

### AudioAPI（`manual/apidocs/AudioAPI_Usage_Examples.md`）
> apidocs上のBaseは `http://localhost:7000/iblink/v1`（`/audio/*`）だが、Dアプリ実装は 7000/8000/7100 が混在するため、利用箇所を分けて列挙する。

- **Retail**
  - `manual/Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.constants.js`
    - `http://localhost:7000/iblink/v1/audio/health`（health）
- **D-Josys / Sales / Medical**
  - **7000/iblink/v1/audio/* を直接叩く実行コードは未検出**（少なくとも現時点の抽出範囲では観測できない）

### AudioNPUAPI（`manual/apidocs/AudioNPUAPI_Usage_Examples.md`）
- **D-Josys**
  - `manual/Dapp/d-josys/src/assets/js/voice/PARealtimeTranscriptionClient.js`（`ws://127.0.0.1:8000/v1/audio/realtime` へWebSocket接続）
- **Sales**
  - `manual/Dapp/d-sales/src/assets/js/voiceSettingsModal.js`
    - 既定 `ws://127.0.0.1:8000/v1/audio/realtime`
    - `http://{derived-from-ws}/health` で健全性待機
- **Medical**
  - `manual/Dapp/d-medical/assets/js/voice/voiceSettingsModal.js`
    - 既定 `ws://127.0.0.1:8000/v1/audio/realtime`
- **Retail**
  - `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/audio_config.js`（既定 `ws://127.0.0.1:8000/v1/audio/realtime` を設定）
  - `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/AudioRealtimeClient.js`（`ws://127.0.0.1:8000/v1/audio/realtime` へWebSocket接続し、PCMをバイナリ送信）
  - `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/AudioServerMicClient.js`（`ws://127.0.0.1:8000/v1/audio/realtime` へWebSocket接続。録音は行わずサーバマイク前提）
  - 併存: `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/RealtimeTranscriptionClient.js`（`http://localhost:7000/realtime` のSignalR Hubを利用）

### EmbeddingsAPI（`manual/apidocs/EmbeddingsAPI_Usage_Examples.md`）
- **Dアプリ実装から `http://localhost:5000/iblink/v1` を直接呼ぶ箇所は未検出**
- ただし、Documents/Retriever のバックエンド構成として Embeddings が前提になっている旨の記述は `docs/index.md` / `manual/apidocs/*` に存在する（= Dアプリからは間接依存になりやすい）。

### LlamaServerAPI（`manual/apidocs/LlamaServerAPI_Usage_Examples.md`）
- **D-Josys**: `manual/Dapp/d-josys/src/utils/LLMResourceManager.js`（既定 `http://localhost:9000/iblink/v1/llama-server`）
- **Sales**: `manual/Dapp/d-sales/src/utils/LLMResourceManager.js`（同上）
- **Retail**: `manual/Dapp/d-retail/src/utils/LLMResourceManager.js`（同上）
- **Medical**: `manual/Dapp/d-medical/resource/LLMResourceManager.js`（同上）

### FoundryLocalAPI（`manual/apidocs/FoundryLocalAPI_Usage_Examples.md`）
- Dアプリ実装（LLMResourceManagerの既定ポリシー）に `http://localhost:9500/iblink/v1/foundry-local` が登場する。
- ただし、少なくとも D-Josys / Sales / Retail の `LLMResourceManager.normalizePolicy()` は LLMモードを `llamaServerApi` に固定しており、**FoundryLocalAPI を実運用で使用する経路は未確定**（= “設定項目として存在” の段階）。

---

## MECE再点検（案B）

### 分類軸（実装で区別できる境界）
- **IB-Link系（`http://localhost:8500/iblink/v1`）**: Documents（`/documents/*`）
- **Retriever（`http://localhost:6500/iblink/v1/retriever`）**
- **Audio（7000系）**
  - AudioAPI（`http://localhost:7000/iblink/v1/audio/*`）
  - Audio Hub（`http://localhost:7000/realtime`）※SignalR Hub（音声イベント/文字起こし）
- **Whisper/Realtime（8000系）**: `ws://127.0.0.1:8000/v1/audio/realtime`（PCM送信）/ `http://{derived}/health` 等
- **音声管理（7100系）**: `http://127.0.0.1:7100/api/whisperserver/*`（start/stop/status…）
- **LLM推論（OpenAI互換 `/v1`）**: `http://localhost:{port}/v1/*`（models/chat-completions）
- **推論サーバ管理**
  - LlamaServerAPI（`http://localhost:9000/iblink/v1/llama-server`）
  - FoundryLocalAPI（`http://localhost:9500/iblink/v1/foundry-local`）

### 判定
- **案B（公式ドキュメント）だけではMECEにならない**
  - 7000/realtime（Hub）と 7100 管理API が `manual/apidocs` に一次情報として存在しない/一致しないため。
- **案B＋「第4章後半（名称未定）」をセットにすると、Dアプリ観測範囲ではMECEに近づく**
  - 境界は「Base URL + Path」で識別可能で、相互に重複しない。
  - 例外（未確定/運用判断が必要）: `FoundryLocalAPI` は設定項目として登場するが、通常経路では無効化されている実装がある。

---

## 不足しているドキュメント（ギャップ）一覧（Dアプリ実装基準）

> “不足”の定義: **Dアプリ実装で使用が観測される**、または章立て上の混同が必ず起きるのに、`docs/api/openapi.*.yaml` と `manual/apidocs` のいずれにも **単独で一次情報として置けるページが存在しない**状態。

### GAP-01: 名称未定（LLM推論エンドポイント: OpenAI互換 `/v1/chat/completions`）
- **対象**: `http://localhost:{port}/v1/models` / `http://localhost:{port}/v1/chat/completions`
- **Dアプリ実装での使用**: D-Josys / Sales / Retail / Medical の各 `src` で利用（`manual/IBUGM/01_DAPP_API_USAGE_MAP.md` の Chat 行が根拠）。
- **なぜ不足か**
  - OpenAPI に Chat が存在しない。
  - `manual/apidocs` には **推論エンドポイント単独の Usage Examples が存在しない**（FoundryLocal の “OpenAI Compatibility” と、LlamaServer の “start後 endpoint が /v1” が断片として存在するのみ）。
- **新設候補（例）**
  - `manual/apidocs/(名称未定)_ChatCompletions_Usage_Examples.md`（※ファイル名/見出しは“正式名称が確定してから”確定する）
  - 収録範囲は最小（Base URL、/v1/models、/v1/chat/completions、messages、stream=SSE、代表レスポンス抽出）に限定。

### GAP-02: 名称未定（音声“管理”エンドポイント: 7100）
- **対象**: `http://127.0.0.1:7100`（音声サーバの起動/停止/状態など）
- **Dアプリ実装での使用**
  - Sales: `manual/Dapp/d-sales/src/assets/js/voiceSettingsModal.js`（既定 `mgmtUrl: 'http://127.0.0.1:7100'`）
  - Retail: `manual/Dapp/d-retail/src/utils/VoiceResourceManager.js`（既定 `http://127.0.0.1:7100`、`/api/whisperserver/{status,health,info,logs,start,stop}` を呼ぶ）
  - Medical: `manual/Dapp/d-medical/assets/js/voice/voiceSettingsModal.js`（既定 `mgmtUrl: 'http://127.0.0.1:7100'`）
- **なぜ不足か**
  - OpenAPI に 7100 の管理APIは存在しない。
  - `manual/apidocs/AudioNPUAPI_Usage_Examples.md` は 8000（Whisper Server）中心で、Dアプリ実装が叩いている `7100/api/whisperserver/*`（起動/停止/状態）の仕様を代表しない。
- **新設候補（例）**
  - `manual/apidocs/(名称未定)_Voice_Management_Usage_Examples.md`（※正式名称が確定してから）

### GAP-03: 名称未定（Audio Hub / Realtime Hub: 7000）
- **対象**: `http://localhost:7000/realtime` / `http://localhost:7000/iblink/v1/audio/health`
- **Dアプリ実装での使用**:
  - Retail: `multilingual.constants.js` に `AUDIO_HUB_URL` / `AUDIO_HEALTH_URL` が定数化
  - Sales: `role_playing/js/*signalr.js` が `hubUrl: 'http://localhost:7000/realtime'` を既定として使用（SignalR）
  - D-Josys / Retail: `assets/js/voice/RealtimeTranscriptionClient.js` が `http://localhost:7000/realtime` を既定として使用（SignalR）
- **なぜ不足か**
  - `manual/apidocs/AudioAPI_Usage_Examples.md` は 7000/iblink/v1/audio/* を説明するが、**Dアプリが参照している 7000/realtime の位置づけが章立てとして別物**になりやすい（“Hub” と “API” が混線する）。
- **新設候補（例）**
  - `manual/apidocs/(名称未定)_AudioHub_Usage_Examples.md`（※正式名称が確定してから）

### GAP-04: “IB-Link経由 Chat”（8500/iblink/v1/chat/completions）の扱い
- **対象**: `http://localhost:8500/iblink/v1/chat/completions`（D-Josys の `IBLinkClient` の baseURL設定次第で到達する可能性）
- **Dアプリ実装での状況**: 実装上は到達可能な構造がある（`manual/IBUGM/01_DAPP_API_USAGE_MAP.md` の Chat 行に記載）。
- **なぜ不足か**
  - OpenAPI に Chat がないため、8500配下の Chat を一次仕様として置けない。
  - 実運用で “使う” のか “互換の残骸” なのか、現状の情報だけでは断定できず、章タイトルに含めると誤解を生む。
- **対応案**
  - 使うことを前提にするなら: OpenAPI と apidocs の両方に追加（=仕様化）。
  - 使わないなら: Dアプリ側で到達不能化/説明から除外し、4.99（競合/混同）に記録する。

---

## 章立て案B（`manual/apidocs` と 1:1 対応）— 公式名称のみを本体に置き、名称未定は後半へ集約する

> 目的: “章タイトル＝バックエンドのサービス単位”に揃え、OpenAPI・apidocs・Dアプリ実装境界の不一致を最小化する。

### 4.6 DocumentsAPI
- apidocs: `manual/apidocs/DocumentsAPI_Usage_Examples.md`
- OpenAPI: `docs/api/openapi.*.yaml`（Documents tag）

### 4.7 RetrieverAPI
- apidocs: `manual/apidocs/RetrieverAPI_Usage_Examples.md`
- OpenAPI: `docs/api/openapi.*.yaml`（Retriever tag）

### 4.8 AudioAPI（IB-Link経由: 7000/iblink/v1/audio/*）
- apidocs: `manual/apidocs/AudioAPI_Usage_Examples.md`
- ※現行 `docs/index.md` の “Audio=8000” と混線しやすいので、Base URLの系統をタイトルで固定する。

### 4.9 AudioNPUAPI（Whisper Server + Realtime: 8000 + WS）
- apidocs: `manual/apidocs/AudioNPUAPI_Usage_Examples.md`
- OpenAPI: `docs/api/openapi.*.yaml`（Audio tag）は 8000 の HTTP（/v1/audio/transcriptions 等）を定義しているため、ここで同期する。

### 4.10 EmbeddingsAPI
- apidocs: `manual/apidocs/EmbeddingsAPI_Usage_Examples.md`
- ※OpenAPI（docs/api）には存在しないため、章として分離して誤解を避ける。

### 4.11 LlamaServerAPI（推論サーバ管理）
- apidocs: `manual/apidocs/LlamaServerAPI_Usage_Examples.md`
- ※“モデル切り替え”という機能名よりも、サービス名（LlamaServerAPI）を前面に出す方が一致する。

### 4.12 FoundryLocalAPI（Foundry Local 管理）
- apidocs: `manual/apidocs/FoundryLocalAPI_Usage_Examples.md`
- ※Dアプリ実装に登場するため、LlamaServerと同列の“管理API”として章を分ける。

---

## 第4章後半（追加/補足）に集約する項目（公式名称なし＝名称未定）

> ここに集約することで、「存在しないAPI名を勝手に付けた」状態を避ける。

### （名称未定）LLM推論エンドポイント（OpenAI互換 `/v1/chat/completions`）
- GAP-01 に対応。
- 章見出しは「名称未定」で固定し、**URL/パス**で識別する。
- **Dアプリ実装での利用箇所（実行コード）**
  - **D-Josys**
    - `manual/Dapp/d-josys/src/assets/js/apiClient.js`（`GET /v1/models` → `POST /v1/chat/completions`、SSE/503待機）
    - `manual/Dapp/d-josys/src/index.js`（IPC: `iblink:chatCompletion` が `POST /v1/chat/completions` を中継）
    - `manual/Dapp/d-josys/src/utils/RAGChatManager.js`（`window.iblink.chatCompletion(messages, ...)`）
    - `manual/Dapp/d-josys/src/assets/js/chat/ChatTransport.js`（`messages` を組み立てて `window.iblink.chatCompletion`）
    - `manual/Dapp/d-josys/src/tech_support_ai/tech_support.js`（`window.iblink.chatCompletion`）
  - **Sales**
    - `manual/Dapp/d-sales/src/assets/js/apiClient.js`（ポリシーからポート解決 → `POST /v1/chat/completions`）
  - **Retail**
    - `manual/Dapp/d-retail/src/main.js`（IPC: `iblink:chatCompletion` が `POST /v1/chat/completions` を中継）
    - `manual/Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.chat.js`（SSE `data:` / `[DONE]` パース）
    - `manual/Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.services.translate.js`（`POST /v1/chat/completions`）
  - **Medical**
    - `manual/Dapp/d-medical/assets/js/apiClient.js`（`GET /v1/models` → `POST /v1/chat/completions`、`report_metadata` 付与）

### （名称未定）音声“管理”エンドポイント（7100）
- GAP-02 に対応。
- **Dアプリ実装での利用箇所（実行コード）**
  - Sales: `manual/Dapp/d-sales/src/assets/js/voiceSettingsModal.js`（既定 `http://127.0.0.1:7100`）
  - Retail: `manual/Dapp/d-retail/src/utils/VoiceResourceManager.js`（`/api/whisperserver/*`）
  - Medical: `manual/Dapp/d-medical/assets/js/voice/voiceSettingsModal.js`（既定 `http://127.0.0.1:7100`）

### （名称未定）Audio Hub / Realtime Hub（7000/realtime 等）
- GAP-03 に対応。
- **Dアプリ実装での利用箇所（実行コード）**
  - D-Josys: `manual/Dapp/d-josys/src/assets/js/voice/RealtimeTranscriptionClient.js`（SignalR: `http://localhost:7000/realtime`）
  - Sales: `manual/Dapp/d-sales/src/role_playing/js/realtimeTranscriptionClient.signalr.js`（SignalR: `http://localhost:7000/realtime`）
  - Sales: `manual/Dapp/d-sales/src/role_playing/js/roleplaySttChatOrchestrator.signalr.js`（既定hubUrlが `http://localhost:7000/realtime`）
  - Retail: `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/RealtimeTranscriptionClient.js`（SignalR: `http://localhost:7000/realtime`）
  - Retail: `manual/Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.constants.js`（`http://localhost:7000/realtime` / `http://localhost:7000/iblink/v1/audio/health`）

### （補足）“IB-Link経由 Chat”（8500/iblink/v1/chat/completions）
- GAP-04 に対応。
- これを「APIとして採用する（=仕様化する）」か「互換の残骸として扱う」かは未確定のため、章タイトルで命名しない。
- **到達可能性がある実装**
  - D-Josys: `manual/Dapp/d-josys/src/api/IBLinkClient.js`（baseURLの与え方次第で 8500/iblink 配下へ到達し得る構造）

---

## 補足：現行 4.6〜4.10 のままでは起きる混同（案Bで解消するもの）
- “Audio API” が **7000（IB-Link経由）/8000（Whisper Server）/7100（管理）/7000(realtime hub)** の複数系統を含んでしまい、実装参照としてMECEにならない。
- “モデル切り替え API” が **LlamaServerAPI** の正式名称と対応せず、apdiocs のドキュメント名と一致しない。
- “Chat API” が OpenAPI 範囲外のため、**仕様の一次置き場が不明**になり、誤記（`message` vs `messages` 等）が混入しやすい。

