# 競合メモ（4.10 EmbeddingsAPI）

本メモは、`docs/index.md` の **4.10 EmbeddingsAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）と Dアプリ実装の差分**を記録する。

---

## CONFLICT-01: OpenAPI（docs/api）に EmbeddingsAPI が存在しない

- **OpenAPI**
  - `docs/api/openapi.(ja|en).yaml` の `paths` に `/embeddings` / `/models` / `/embeddings/health` が存在しない
- **apidocs**
  - `manual/apidocs/EmbeddingsAPI_Usage_Examples.md` が `http://localhost:5000/iblink/v1` の Usage Examples を提供している

**判断**:
- `docs/index.md` 側は **apidocs を一次情報**として記述する。
- 仕様として OpenAPI に統合する場合は、OpenAPI 側に EmbeddingsAPI の `servers/paths/schemas` を追加する。

---

## CONFLICT-02: Dアプリ実装からの直接呼び出しが未検出

- **Dアプリ実装**
  - 現時点の抽出範囲では `http://localhost:5000/iblink/v1/*` の直接呼び出しは未検出
- **apidocs**
  - フロントエンドから直接叩ける形（OpenAI互換の `/embeddings` 等）として例示されている

**判断**:
- 本節（4.10）は「将来フロントエンドが直接利用する可能性があるAPI」として一次情報を残す。
- Dアプリ実装の根拠が不足しているため、「Dアプリが本APIを必ず直接呼ぶ」とは断定しない。

---

## 更新履歴
- 2026-02-27: 初版作成（EmbeddingsAPIの章整備に伴う差分整理）

