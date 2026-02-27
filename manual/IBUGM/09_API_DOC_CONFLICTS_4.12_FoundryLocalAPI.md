# 競合メモ（4.12 FoundryLocalAPI）

本メモは、`docs/index.md` の **4.12 FoundryLocalAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）とDアプリ実装の差分**を記録する。

---

## CONFLICT-01: OpenAPI（docs/api）に FoundryLocalAPI が存在しない

- **OpenAPI**
  - `docs/api/openapi.(ja|en).yaml` の `paths` に `http://localhost:9500/iblink/v1/foundry-local/*` が存在しない
- **apidocs**
  - `manual/apidocs/FoundryLocalAPI_Usage_Examples.md` が Usage Examples を提供している

**判断**:
- `docs/index.md` の 4.12 は **apidocs を一次情報**として記述する。
- 仕様として OpenAPI に統合する場合は、OpenAPI側に FoundryLocalAPI の `servers/paths/schemas` を追加する。

---

## CONFLICT-02: OpenAI互換の `GET /v1/models` が Base URL 配下ではない

- **FoundryLocalAPI（管理API）**
  - Base URL: `http://localhost:9500/iblink/v1/foundry-local`
- **OpenAI互換**
  - `GET http://localhost:9500/v1/models`（Base URL 直下ではない）
  - 起動後の推論 endpoint は `http://127.0.0.1:{port}/v1`（`api_key` 付き）

**判断**:
- 4.12 では `/v1/*` を「起動後に得られる推論Endpoint」としてのみ扱い、詳細仕様は **第4章後半（名称未定）**側へ分離する。

---

## CONFLICT-03: Dアプリ実装で FoundryLocalAPI は“設定項目として存在”するが、実運用経路が固定で無効化されている可能性がある

- **Dアプリ実装**
  - `LLMResourceManager.getDefaultPolicy().foundryLocalApi.apiBaseUrl` に `http://localhost:9500/iblink/v1/foundry-local` が登場
  - ただし `normalizePolicy()` が `llm.mode = "llamaServerApi"` に固定している実装がある（D-Josys / Sales / Retail）

**判断**:
- 4.12 では「Dアプリが本APIを必ず直接呼ぶ」とは断定しない。
- 既存実装に合わせる場合は、まず `normalizePolicy()` の固定方針（FoundryLocalを許可するか）を整理してから採用する。

---

## 更新履歴
- 2026-02-27: 初版作成（FoundryLocalAPIの章整備に伴う差分整理）

