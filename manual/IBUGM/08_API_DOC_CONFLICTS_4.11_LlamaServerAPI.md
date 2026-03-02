# 競合メモ（4.11 LlamaServerAPI）

本メモは、`docs/index.md` の **4.11 LlamaServerAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）とDアプリ実装の差分**を記録する。

---

## CONFLICT-01: OpenAPI（docs/api）に LlamaServerAPI が存在しない

- **OpenAPI**
  - `docs/api/openapi.(ja|en).yaml` の `paths` に `http://localhost:9000/iblink/v1/llama-server/*` が存在しない
- **apidocs**
  - `manual/apidocs/LlamaServerAPI_Usage_Examples.md` が Usage Examples を提供している

**判断**:
- `docs/index.md` の 4.11 は **apidocs を一次情報**として記述する。
- 仕様として OpenAPI に統合する場合は、OpenAPI側に LlamaServerAPI の `servers/paths/schemas` を追加する。

---

## CONFLICT-02: `GET /health` の Base URL が他Endpointと異なる

- **apidocs**
  - 管理API: `http://localhost:9000/iblink/v1/llama-server/*`
  - ヘルス: `http://localhost:9000/health`（Base URL 直下）

**判断**:
- `docs/index.md` では「混線防止」として明示し、`/iblink/v1/llama-server/health` と誤認しないようにする。

---

## CONFLICT-03: 推論Endpoint（OpenAI互換 `/v1/*`）は本APIの管理対象だが、LlamaServerAPI 自体の `paths` ではない

- **apidocs**
  - `POST /start` / `POST /switch-model` のレスポンスに `endpoint: "http://localhost:{port}/v1"` が含まれる
  - ただし、その `/v1/*`（例: `/v1/chat/completions`）は LlamaServerAPI の `Base URL` 直下ではない

**判断**:
- 4.11 では `/v1/*` を「起動後に得られる推論Endpoint」としてのみ扱い、詳細仕様は **第4章後半（名称未定）**側へ分離する。

---

## CONFLICT-04: Dアプリ実装からの直接呼び出しが未検出

- **Dアプリ実装（実行コード）**
  - 現時点の抽出範囲では `http://localhost:9000/iblink/v1/llama-server` の直接呼び出しは未検出
- **apidocs**
  - フロントエンドから直接叩ける形（start/stop/status/logs等）として例示されている

**判断**:
- 本節（4.11）は一次情報として保持しつつ、「Dアプリが本APIを必ず直接呼ぶ」とは断定しない。

---

## 更新履歴
- 2026-02-27: 初版作成（LlamaServerAPIの章整備に伴う差分整理）

