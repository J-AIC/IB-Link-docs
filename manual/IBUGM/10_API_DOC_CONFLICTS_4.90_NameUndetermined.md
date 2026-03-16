# 競合メモ（4.13〜4.15：公式名称なし）

本メモは、`docs/index.md` の **4.13〜4.15（公式名称なし）** を「Dアプリ実装参照向け」に整備する過程で観測した、**旧記述とDアプリ実装（事実）の差分**を記録する。

---

## CONFLICT-01: LLM推論の Base URL / Path（旧記述が `.../iblink/v1` になっていた）

- **旧 `docs/index.md`（修正前）**
  - Base URL: `http://localhost:8080/iblink/v1`
  - Path: `POST /chat/completions`
- **Dアプリ実装（推論）**
  - Base URL: `http://localhost:{port}`（既定 8080 等）
  - Path: `POST /v1/chat/completions`
  - 根拠:
    - `manual/Dapp/d-josys/src/assets/js/apiClient.js`（`fetch(`${RAG_CHAT_BASE_URL}/v1/chat/completions`, ...)`）
    - `manual/Dapp/d-retail/src/main.js`（`fetch(`${base}/v1/chat/completions`, ...)`）
    - `manual/Dapp/d-medical/assets/js/apiClient.js`（`requestUrl = `${baseUrl}/v1/chat/completions``）

**判断**: LLM推論は **`/v1/*`** として記述し、`.../iblink/v1` と混線させない。

---

## CONFLICT-02: `message` vs `messages`（旧記述が `message: [...]` になっていた）

- **旧 `docs/index.md`（修正前）**
  - `message: [...]`
- **Dアプリ実装（送信）**
  - `messages: [...]`（role/content の配列）
  - 根拠:
    - `manual/Dapp/d-josys/src/assets/js/apiClient.js`（`chatRequest = { ..., messages, ... }`）
    - `manual/Dapp/d-medical/assets/js/apiClient.js`（`buildReportGenerationRequest()` が `messages: [...]` を構築）
    - `manual/Dapp/d-retail/src/main.js`（`body.messages = ...`）

**判断**: `messages` に統一し、`message` は採用しない（一次仕様にも実装にも根拠がない）。

---

## CONFLICT-03: ストリーミングの表現（SSE）

- **Dアプリ実装**
  - `stream:true` の場合、SSE（`data: {json}\n` / `[DONE]`）を行単位で解析する実装がある（Retail）
  - 根拠: `manual/Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.chat.js`

**判断**: マニュアルでは「SSE（data行）を行単位で処理する」ことだけを残し、未確認のHTTPステータス等は断定しない。

---

## CONFLICT-04: `api_key` を伴う推論Endpoint（Authorizationヘッダが必要）

- **管理API（FoundryLocalAPI）**
  - `POST /start` のレスポンスに `endpoint: "http://127.0.0.1:{port}/v1"` と `api_key` が含まれる
- **推論API（/v1/chat/completions）**
  - `api_key` がある場合、`Authorization: Bearer {api_key}` を送る例がある
  - 根拠: `manual/apidocs/FoundryLocalAPI_Usage_Examples.md`（workflow例）

**判断**: 4.13 では `api_key` の存在と `Authorization: Bearer` の送信例のみを示し、認証方式の断定は避ける。

---

## NOTE-01: 音声管理エンドポイント（7100）の起動/停止パラメータと安全策

- **起動（POST /api/whisperserver/start）**
  - body に `model` / `port` / `host` / `detached` を含める実装があります（未指定の場合はサーバ側既定に委ねる）。
- **停止（POST /api/whisperserver/stop）**
  - body は `{}` の実装があります。
  - 誤停止を避けるため「自分で起動したセッションのみ停止する」等のガードを入れる実装があります（例: `startedByApp` を保持し、強制停止フラグを別途設ける）。

---

## NOTE-02: 7000/realtime（SignalR）のイベント名/完了フラグ/音声送信の形

- **受信イベント名**
  - `TranscriptionResult` を購読する実装があります。
  - 互換のため `Transcription` / `PartialResult` / `FinalResult` も購読する実装があります。
- **完了フラグ**
  - `phrase_complete` / `is_final` / `final` / `type: "final"` 等を完了判定に使う実装があります。
- **音声送信**
  - `SendAudio` には `Uint8Array` そのものではなく、`Array<number>`（例: `Array.from(new Uint8Array(int16Pcm.buffer))`）を渡す実装があります。
  - 終了時に `FlushAudio` を呼ぶ実装があります。

---

## 更新履歴
- 2026-02-27: 初版作成（公式名称なしセクションの事実整備）

