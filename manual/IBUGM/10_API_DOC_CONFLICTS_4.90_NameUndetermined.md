# 競合メモ（4.13〜4.16：公式名称なし）

本メモは、`docs/index.md` の **4.13〜4.16（公式名称なし）** を「Dアプリ実装参照向け」に整備する過程で観測した、**旧記述とDアプリ実装（事実）の差分**を記録する。

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

## 更新履歴
- 2026-02-27: 初版作成（公式名称なしセクションの事実整備）

