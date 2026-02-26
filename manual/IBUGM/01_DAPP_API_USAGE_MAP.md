## Dアプリ別 API使用箇所マップ（MECE）

### 目的
- 4.6〜4.10（Chat / Documents / Retriever / Audio / モデル切り替え）のドキュメント修正に先立ち、**各Dアプリの実装内で実際に使われているAPI**を「どこで／何を」単位でMECEに整理する。

---

## 重要な前提（2026-02-26 時点の事実）

### 実装コードの有無
- `manual/Dapp/d-retail/`
- `manual/Dapp/d-medical/`
- `manual/Dapp/d-josys/`
- `manual/Dapp/d-sales/`

上記ディレクトリに実装コードが存在することを確認済み（※ `D-Josys` / `D-sales` は `.git/index` のみだが、別途 `d-josys` / `d-sales` に実体コードがある）。

---

## MECE分類（API種別）

本マップは、各アプリについて以下5分類に **必ず**割り当てる（重複は「競合/重複利用」として別欄に記録）。

1. **Chat API**（4.6）
2. **Documents API**（4.7）
3. **Retriever API**（4.8）
4. **Audio API**（4.9）
5. **モデル切り替え API**（4.10）

---

## D-Josys（最優先）

| API種別 | 使用箇所（ファイル/関数） | 呼び出し（URL/Path） | Request（キー差分含む） | Response（処理） | 根拠 |
|---|---|---|---|---|---|
| Chat | `src/assets/js/apiClient.js`（RAG Chat / /v1/models で到達性確認）<br>`src/api/IBLinkClient.js: chatCompletion()`（/chat/completions） | **Chat(OpenAI互換)**: `http://localhost:8080/v1/chat/completions`<br>**Model list**: `http://localhost:8080/v1/models`<br>**IB-Link経由**: `http://localhost:8500/iblink/v1/chat/completions`（baseURLを8500にした場合） | `messages` を使用（system+user）<br>`stream` を考慮（ただし `apiClient.js` の `ragChatCompletions` は `stream:false`） | `503` の `Loading model` を検知して再試行する分岐あり | `manual/Dapp/d-josys/src/assets/js/apiClient.js` L5-L7, L102-L123, L227-L257, L288-L306<br>`manual/Dapp/d-josys/src/api/IBLinkClient.js` L274-L279 |
| Documents | `src/api/IBLinkClient.js: processDocuments/getDocumentStatus/listDocuments/deleteDocument/searchDocuments()`<br>`src/tech_support_ai/delete_all_server_docs.js`（直接fetch） | `http://localhost:8500/iblink/v1/documents/process|status|list|delete|search` | 必須: `d_app_id`, `project_id`（+ endpointごとに `files`/`job_id`/`query` 等） | `409` を `DUPLICATE`、`400` を `INVALID_ARGUMENT` として例外化 | `manual/Dapp/d-josys/src/api/IBLinkClient.js` L7-L13, L166-L253<br>`manual/Dapp/d-josys/src/tech_support_ai/delete_all_server_docs.js`（/documents/delete の直接呼び出しは grep で検出済み） |
| Retriever | **未使用（少なくとも `/retriever` 呼び出しは `src` から未検出）** | - | - | - | `manual/Dapp/d-josys/src` を `/retriever` で検索→一致0件 |
| Audio | `src/assets/js/voice/PARealtimeTranscriptionClient.js`（WebSocket realtime） | `ws://127.0.0.1:8000/v1/audio/realtime` | `action:start` + `config`（model/language/response_format/sample_rate/vad_enabled/energy_threshold/record_timeout/phrase_timeout）をJSON送信し、その後PCMバイナリ送信 | 受信はJSON。`error` フィールドがあれば例外化。`partial/final` を判定してコールバック | `manual/Dapp/d-josys/src/assets/js/voice/PARealtimeTranscriptionClient.js` L3-L20, L298-L314, L316-L320, L419-L445 |
| モデル切替 | `src/utils/LLMResourceManager.js`（LlamaServerAPI 管理）<br>`src/index.js` 初期化 | `http://localhost:9000/iblink/v1/llama-server/{status,models,info,start,stop}` | `POST /start`: `{ model_path, port, (server_config|options), (binary_path) }` | `_fetchJson` で text→JSON をベストエフォート。HTTP非2xxは `HTTP_ERROR` | `manual/Dapp/d-josys/src/utils/LLMResourceManager.js` L14-L49, L176-L283<br>`manual/Dapp/d-josys/src/index.js` L241-L273（初期化） |

---

## Sales（次優先）

| API種別 | 使用箇所（ファイル/関数） | 呼び出し（URL/Path） | Request（キー差分含む） | Response（処理） | 根拠 |
|---|---|---|---|---|---|
| Chat | `src/assets/js/apiClient.js`（LLM自動起動を含む）<br>`src/api/IBLinkClient.js: chatCompletion()` | `http://localhost:8080/v1/chat/completions`（ragBase） | `messages` を使用（例: `{ model, messages, max_tokens, temperature, stream }`） | `IBLinkClient.request()` は `options.stream` 時 `response.body` を返す | `manual/Dapp/d-sales/src/assets/js/apiClient.js` L28-L46（ragBase解決）<br>`manual/Dapp/d-sales/src/api/IBLinkClient.js` L216-L221 |
| Documents | `src/api/IBLinkClient.js: processDocuments/status/list/delete/search`<br>`src/preload.js: window.iblinkProcessDocuments`（固定URL直叩き） | `http://localhost:8500/iblink/v1/documents/process|status|list|delete|search` | `preload.js` の `iblinkProcessDocuments` は `duplicate_strategy:'sync'` を固定し、`files` を `{file_path, enable_ocr}` に整形して送信 | `IBLinkClient` は error body を `response.json()` で解析（失敗時は `{}`） | `manual/Dapp/d-sales/src/api/IBLinkClient.js` L111-L195<br>`manual/Dapp/d-sales/src/preload.js` L90-L117 |
| Retriever | **本番コード（`src`直下）では未確定**。一方、`src/Tasks/cf/renderer.js` に RetrieverAPI 検証用の `fetch` が存在 | `POST ${apiUrl}/iblink/v1/retriever` | `text, d_app_id, project_id, limit, search_mode`（+ optional filters） | `response.json()` をログ出力し `renderSearchResults` | `manual/Dapp/d-sales/src/Tasks/cf/renderer.js` L1188-L1232 |
| Audio | `src/assets/js/voiceSettingsModal.js`（WS URL + mgmt URL を保持し /health で疎通確認）<br>`src/role_playing/js/realtimeAudio.config.js`（既定URL） | `ws://127.0.0.1:8000/v1/audio/realtime`（既定）<br>`http://127.0.0.1:7100`（管理API）<br>`http://localhost:8000/health`（wsから派生したHTTP baseで確認） | `localStorage` に `wsUrl/mgmtUrl/model/stopOnQuit` 等を保存 | `/health` の JSON を読み、`status:healthy` + `whisper.status` を条件に待機 | `manual/Dapp/d-sales/src/assets/js/voiceSettingsModal.js` L11-L18, L97-L115<br>`manual/Dapp/d-sales/src/role_playing/js/realtimeAudio.config.js` L2-L5 |
| モデル切替 | `src/utils/LLMResourceManager.js`（D-Josys互換のLlamaServerAPI管理）<br>`src/index.js` 初期化<br>`src/preload.js: window.llmManager`（IPC） | `http://localhost:9000/iblink/v1/llama-server/*`（既定） | `window.llmManager.start({ modelPath, port, options, customArgKey, customArgValue, customArgsOther, timeoutMs })` を使用する実装が存在 | `before-quit` で `llamaStop(forceStop:false)` を条件付き実行 | `manual/Dapp/d-sales/src/index.js` L555-L590<br>`manual/Dapp/d-sales/src/preload.js` L16-L37 |

---

## Retail（次優先）

| API種別 | 使用箇所（ファイル/関数） | 呼び出し（URL/Path） | Request（キー差分含む） | Response（処理） | 根拠 |
|---|---|---|---|---|---|
| Chat | `src/main.js: ipcMain.handle('iblink:chatCompletion')`（Main側でHTTP中継）<br>`src/D-Retail/product_assistant/product_assistant.services.rag.js`（HTTP/IPC両対応）<br>`src/D-Retail/product_assistant/product_assistant.services.chat.js`（stream:true でSSE読取） | `http://localhost:${port}/v1/chat/completions`（portはポリシー: 既定8080） | `messages` を送信。`product_assistant.services.chat.js` は `stream:true` を使用 | `stream:true` の場合 `Response.body` を `TextDecoder` で読み、`data: {json}\n` を行単位でパース（`[DONE]` も扱う） | `manual/Dapp/d-retail/src/main.js` L675-L703<br>`manual/Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.rag.js` L152-L174<br>`manual/Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.chat.js` L199-L234 |
| Documents | `src/main.js: iblink:processDocuments / iblink:deleteDocument / iblink:searchDocuments`（Main側）<br>`src/main.js: documents:bulkDelete-start`（背景削除） | `http://localhost:8500/iblink/v1/documents/process|delete|search` | `processDocuments`: `project_id` が `proj_default` の場合ゼロUUIDへ正規化して送信 | 受信は `resp.text()` → JSONをベストエフォートで復元し、非2xxは `{success:false,status,error,data}` を返す | `manual/Dapp/d-retail/src/main.js` L502-L607, L610-L644, L646-L673 |
| Retriever | **未使用（少なくとも `/retriever` 呼び出しは `src` から未検出）** | - | - | - | `manual/Dapp/d-retail/src` を `/retriever` で検索→一致0件 |
| Audio | `src/D-Retail/*/index.html`（設定UIの表示）<br>`src/D-Retail/assets/js/voice/*`（WSクライアント）<br>`src/utils/VoiceResourceManager.js`（mgmt 7100）<br>`src/D-Retail/multilingual_service/multilingual.constants.js`（Audio Hub 7000） | **WS realtime**: `ws://127.0.0.1:8000/v1/audio/realtime`（既定）<br>**管理API**: `http://127.0.0.1:7100`（既定）<br>**Audio Hub**: `http://localhost:7000/realtime` / `http://localhost:7000/iblink/v1/audio/health` | localStorageに `ws_voice_api_url` / `ws_voice_mgmt_api_url` などを保持する実装が存在 | - | `manual/Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.constants.js` L6-L13<br>（WS既定URL等は grep で多数検出済み） |
| モデル切替 | `src/utils/LLMResourceManager.js`（LlamaServerAPI 管理）<br>`src/main.js: llm:* IPC`（policy/status/start/stop など） | `http://localhost:9000/iblink/v1/llama-server/*`（既定） | `llm:status` は `llamaStatus(policy)` を呼び `mode:'llamaServerApi'` を付けて返す | - | `manual/Dapp/d-retail/src/main.js` L706-L736<br>`manual/Dapp/d-retail/src/utils/LLMResourceManager.js`（ヘッダコメント/既定URLは grep で検出済み） |

---

## Medical（最後）

| API種別 | 使用箇所（ファイル/関数） | 呼び出し（URL/Path） | Request（キー差分含む） | Response（処理） | 根拠 |
|---|---|---|---|---|---|
| Chat | `d-medical/assets/js/apiClient.js: callChatAPI()`（/v1/models で到達性確認→送信） | `http://localhost:${port}/v1/chat/completions`（portはポリシー: 既定8080）<br>`http://localhost:${port}/v1/models`（ready確認） | `messages`（system+user）/ `max_tokens` / `temperature` / `stream` / `report_metadata` などをpayloadに含める実装が存在 | エラー時は `response.json()` 失敗なら `response.text()` を `message` として扱う | `manual/Dapp/d-medical/assets/js/apiClient.js` L45-L70, L141-L180, L245-L262 |
| Documents | **未使用（少なくとも `/documents/*` 呼び出しは `d-medical` から未検出）** | - | - | - | `manual/Dapp/d-medical` を `/documents/` で検索→一致0件 |
| Retriever | **未使用（少なくとも `/retriever` 呼び出しは `d-medical` から未検出）** | - | - | - | `manual/Dapp/d-medical` を `/retriever` で検索→一致0件 |
| Audio | `d-medical/main.js: buildAudioConfig()`（WS URL生成）<br>`d-medical/assets/js/voice/voiceSettingsModal.js`（localStorage設定） | `http://localhost:8000`（base）<br>`ws(s)://.../v1/audio/realtime` と `.../v1/audio/stream` を env/既定から組み立て | localStorageキー（D-Josys互換）: `ws_voice_api_url`, `ws_voice_mgmt_api_url`, `ws_voice_model` | - | `manual/Dapp/d-medical/main.js` L7-L74<br>`manual/Dapp/d-medical/assets/js/voice/voiceSettingsModal.js` L7-L21, L77-L85 |
| モデル切替 | `d-medical/resource/LLMResourceManager.js`（管理API）<br>`d-medical/main.js: initResourceManagers()` | `http://localhost:9000/iblink/v1/llama-server/{status,models,info,start,stop}`（既定） | `POST /start`: `{ model_path, port, options, (binary_path) }`（customArgKey等は options側に入れる実装） | `_fetchJson` は `text` を読んでJSON化（非2xxは例外） | `manual/Dapp/d-medical/resource/LLMResourceManager.js` L6-L16, L165-L177, L180-L217<br>`manual/Dapp/d-medical/main.js` L83-L96 |

---

## 競合/重複利用（4.99候補の起票単位）

現時点では実装未取得のため、競合は起票できない（事実がない）。
実装が揃い次第、以下を競合IDの単位とする。

- **CONFLICT候補（例）**
  - Chat API の baseUrl/パス（`/iblink/v1` の有無）がアプリ間で異なる
  - Chat API の requestキー（`message` vs `messages`）がアプリ間で異なる
  - Documents API の `list` が GET/POST で異なる（OpenAPIとの差分含む）
  - Audio API の WebSocket を利用する/しないがアプリ間で異なる
  - モデル切り替え API の利用有無・ポートがアプリ間で異なる

---

## APIドキュメント種別（Chat/Documents/Retriever/Audio/モデル切替）がMECEか？

### 結論（現時点の実装根拠ベース）
- **現行の5分類だけでは不足**する可能性が高い。
  - 理由: Dアプリ実装上、同じ「音声」でも **少なくとも3系統**が混在している（例: 8000のAudio API、7100の管理API、7000のHub/health）。
  - 同様に「LLM」も **推論（8080の `/v1/*`）** と **管理（9000の `/iblink/v1/llama-server/*`）** が分離している。

### 追加候補（実装で観測された“別カテゴリ”）
- **Voice 管理API（7100）**: `http://127.0.0.1:7100`（D-Sales/D-Retail/D-Medicalで既定値として登場）
- **Audio Hub / Realtime Hub（7000）**: `http://localhost:7000/realtime` / `http://localhost:7000/iblink/v1/audio/health`（D-Retailで定数化）
- **Foundry Local API（9500）**: `http://localhost:9500/iblink/v1/foundry-local`（D-Josys/D-Salesで既定値として登場）

> 上記を 4.6〜4.10 のどこに含めるか（新設するか）は、次工程（ドキュメント修正）で **実装根拠とOpenAPIの範囲**を揃えて決定する。

---

## 関連
- 計画書: `manual/IBUGM/00_API_DOC_REWRITE_PLAN.md`
- OpenAPI: `docs/api/openapi.ja.yaml`

