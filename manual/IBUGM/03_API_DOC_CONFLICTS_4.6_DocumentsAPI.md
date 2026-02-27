# 競合メモ（4.6 DocumentsAPI）

本メモは、`docs/index.md` の **4.6 DocumentsAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）と既存実装、または旧ドキュメント記述間の差分**を記録する。

---

## CONFLICT-01: `/documents/list` のHTTPメソッド（旧ドキュメント誤記）

- **旧 `docs/index.md`（修正前）**
  - `GET /documents/list` と記載
- **OpenAPI**
  - `POST /documents/list`（`docs/api/openapi.*.yaml`）
- **apidocs**
  - `POST /documents/list`（`manual/apidocs/DocumentsAPI_Usage_Examples.md`）
- **Dアプリ実装**
  - `POST /documents/list`（`manual/Dapp/*/src/api/IBLinkClient.js` の `listDocuments()`）

**判断**: 旧ドキュメントの `GET` は誤記。`POST` に統一。

---

## CONFLICT-02: `/documents/search` の `search_mode` パラメータ（実装で観測、OpenAPI未記載）

- **OpenAPI**
  - `DocumentSearchRequest` に `search_mode` が存在しない（`docs/api/openapi.*.yaml`）
- **Dアプリ実装（送信例）**
  - `manual/Dapp/d-josys/src/assets/js/apiClient.js`（`search_mode: "hybrid"` を送信）
  - `manual/Dapp/d-sales/src/api/IBLinkClient.js`（`search_mode: "hybrid"` を送信）

**判断**:
- バックエンドが受理している（または無視している）可能性があり、現時点では **「実装例として扱い、仕様（必須/有効値）として断定しない」**。
- 仕様化する場合は OpenAPI 側へ `search_mode` を追加する。

---

## CONFLICT-03: `/documents/health` の一次仕様の位置づけ（apidocsに記載、OpenAPIに未定義）

- **apidocs**
  - `GET /documents/health` の例が存在（`manual/apidocs/DocumentsAPI_Usage_Examples.md`）
- **OpenAPI**
  - `paths` に `/documents/health` が存在しない（`docs/api/openapi.*.yaml`）
- **Dアプリ実装**
  - 現時点の抽出範囲では直接呼び出し未検出

**判断**:
- OpenAPI の範囲（Documents tag）に寄せるなら `/documents/health` を OpenAPI に追加する。
- 追加しない場合、マニュアル側では「apidocs上の補足（OpenAPI未収録）」として扱う。

---

## CONFLICT-04: `/documents/search` の必須パラメータ（OpenAPIと実装の“最小”が一致しない可能性）

- **OpenAPI**
  - 必須は `query` のみ（`DocumentSearchRequest.required: [query]`）
- **Dアプリ実装**
  - `d_app_id` / `project_id` を付与する実装と、省略する実装が混在する可能性がある（例: D-Retail の Main 中継実装は `query` と `project_id` のみ組み立てる箇所がある）

**判断**:
- 現行の一次仕様（OpenAPI）に合わせ、マニュアルでは **必須を `query` としつつ、`d_app_id` / `project_id` は実装で使う前提項目として例示**する。
- Dアプリ間で「必須扱い」が異なる場合は、各アプリの呼び出し箇所を根拠として追記する。

---

## 更新履歴
- 2026-02-27: 初版作成（DocumentsAPIの章リライトに伴う差分整理）

