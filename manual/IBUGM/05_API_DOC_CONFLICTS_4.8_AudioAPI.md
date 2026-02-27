# 競合メモ（4.8 AudioAPI）

本メモは、`docs/index.md` の **4.8 AudioAPI（IB-Link経由: 7000/iblink/v1/audio/*）** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）と Dアプリ実装の差分**を記録する。

---

## CONFLICT-01: Audio の OpenAPI（docs/api）と apidocs の Base URL / Path が一致しない

- **apidocs（AudioAPI）**
  - Base URL: `http://localhost:7000/iblink/v1`
  - 例: `POST /audio/transcriptions`
  - 例: `GET /audio/health`
  - 例: `GET /audio/system/info`
  - 根拠: `manual/apidocs/AudioAPI_Usage_Examples.md`
- **OpenAPI（docs/api）**
  - servers: `http://localhost:8000`
  - 例: `POST /v1/audio/transcriptions`
  - 例: `GET /health`, `GET /status`
  - 根拠: `docs/api/openapi.*.yaml`（Audio tag）

**判断**:
- 7000 と 8000 は **別系統**として章を分離して扱う必要がある（案Bの 4.8 / 4.9 の分離に対応）。

---

## CONFLICT-02: Dアプリ実装での AudioAPI（7000/iblink/v1/audio/*）の利用が限定的

- **Retail**
  - `http://localhost:7000/iblink/v1/audio/health` が定数として存在
  - 根拠: `manual/Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.constants.js`
- **他Dアプリ（D-Josys / Sales / Medical）**
  - 現時点の抽出範囲では、7000/iblink/v1/audio/* を直接呼ぶ実行コードは未検出

**判断**:
- マニュアル（4.8）では apidocs を一次情報として保持しつつ、Dアプリ側の採用状況（現状はヘルスURL程度）を併記する。

---

## 更新履歴
- 2026-02-27: 初版作成（AudioAPIの章整備に伴う差分整理）

