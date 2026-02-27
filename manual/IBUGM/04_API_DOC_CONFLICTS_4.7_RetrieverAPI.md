# 競合メモ（4.7 RetrieverAPI）

本メモは、`docs/index.md` の **4.7 RetrieverAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）と既存実装、またはDアプリ間の採用方針**の差分を記録する。

---

## CONFLICT-01: Base URL の切り出し方（OpenAPI と apidocs の表現差）

- **OpenAPI**
  - servers: `http://localhost:6500/iblink/v1`
  - paths: `POST /retriever`, `GET /retriever/health`, `GET /retriever/info`
- **apidocs**
  - Base URL: `http://localhost:6500/iblink/v1/retriever`
  - 例: `POST http://localhost:6500/iblink/v1/retriever`
  - 例: `GET  http://localhost:6500/iblink/v1/retriever/health`

**判断**: どちらも到達するURLは同等（Base+Pathの切り出しが異なるだけ）。`docs/index.md` では **Base URL を `.../iblink/v1` に揃え、Path を `/retriever*` で記載**し、混線を防ぐ。

---

## CONFLICT-02: Dアプリによる採用方針の差（D-Josys は RetrieverAPI を無効化）

- **D-Josys**
  - Main側で `iblink:documentRetriever` を 501 で返し、明示的に無効化している
  - 代替として DocumentsAPI の `POST /documents/search` を使うよう誘導している
    - 根拠: `manual/Dapp/d-josys/src/index.js`
- **Sales**
  - 検証用UI（Tasks）で `POST ${apiUrl}/iblink/v1/retriever` を実行している
    - 根拠: `manual/Dapp/d-sales/src/Tasks/cf/renderer.js`
- **Retail / Medical**
  - 現時点の実装コードでは RetrieverAPI 呼び出しは未検出

**判断**:
- RetrieverAPI を「Dアプリが必ず使うAPI」として断定できない。
- `docs/index.md` では **仕様の一次情報（OpenAPI/apidocs）を軸**に説明しつつ、Dアプリ実装の現状（D-Josysは無効化、Salesは検証用）を併記する。

---

## 更新履歴
- 2026-02-27: 初版作成（RetrieverAPIの章リライトに伴う差分整理）

