# 競合メモ（4.9 AudioNPUAPI）

本メモは、`docs/index.md` の **4.9 AudioNPUAPI** を「Dアプリ実装参照向け」に整備する過程で観測した、**仕様（OpenAPI / apidocs）と Dアプリ実装、またはDアプリ間の差分**を記録する。

---

## CONFLICT-01: OpenAPI（docs/api）の Audio は WebSocket を定義していないが、Dアプリは WS realtime を利用している

- **OpenAPI（docs/api/openapi.*.yaml）**
  - `http://localhost:8000` の HTTP: `GET /health`, `GET /status`, `POST /v1/audio/transcriptions`, `POST /v1/audio/translations`
  - WebSocket の定義は存在しない
- **apidocs（manual/apidocs/AudioNPUAPI_Usage_Examples.md）**
  - WebSocket の章があり、`/v1/audio/stream` と `/v1/audio/realtime` の例がある
- **Dアプリ実装**
  - WS `ws://127.0.0.1:8000/v1/audio/realtime` を利用
    - 例: `manual/Dapp/d-josys/src/assets/js/voice/PARealtimeTranscriptionClient.js`
    - 例: `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/AudioRealtimeClient.js`
    - 例: `manual/Dapp/d-medical/assets/js/voice/RealtimeAudioClient.js`

**判断**:
- `docs/index.md` では「Dアプリ実装の一次情報」として WS realtime を説明対象に含める（ただし OpenAPI に未収録である点は明示）。
- 仕様化（OpenAPI に統合）する場合は、別途 WS のプロトコル/メッセージ仕様を整理してから追記する。

---

## CONFLICT-02: WS `/v1/audio/realtime` の開始設定ペイロードがDアプリ間で一致しない

- **D-Josys**
  - `{"action":"start","config":{...}}` 形式を送信
  - 根拠: `manual/Dapp/d-josys/src/assets/js/voice/PARealtimeTranscriptionClient.js`（`_sendStartPayload()`）
- **Retail**
  - `{ language, energy_threshold, ... }` の設定オブジェクトを直接送信（`action` ラッパなし）
  - 根拠: `manual/Dapp/d-retail/src/D-Retail/assets/js/voice/AudioRealtimeClient.js`（`onopen` で `cfg` を送信）

**判断**:
- 現時点ではサーバ側が両形式を受理している可能性があるが、互換性を断定しない。
- マニュアル側では **「実装差分」として両方式を併記**し、アプリ側は既存クライアント実装に合わせる前提で記述する。

---

## CONFLICT-03: WS のエンドポイント `/v1/audio/stream`（apidocs）と `/v1/audio/realtime`（Dアプリ採用）が混在

- **apidocs**
  - `ws://localhost:8000/v1/audio/stream` の例が存在
  - `ws://localhost:8000/v1/audio/realtime` の例も存在
- **Dアプリ実装**
  - 現時点の抽出範囲では `/v1/audio/realtime` の利用が中心（`/v1/audio/stream` は未検出）

**判断**:
- `docs/index.md` の 4.9 は **Dアプリで採用されている `/v1/audio/realtime` を軸**に記載する。
- `/v1/audio/stream` は採用が確認できないため、本節の必須事項としては扱わない（必要になった段階で採用根拠を追加する）。

---

## CONFLICT-04: `localhost` と `127.0.0.1` の使い分け

- **apidocs**
  - `127.0.0.1:8000` を出力例として記載する箇所と、`localhost:8000` を例示する箇所が混在
- **Dアプリ実装**
  - `ws://127.0.0.1:8000/v1/audio/realtime` を既定にする例（D-Josys）
  - `ws://localhost:8000/v1/audio/realtime` を既定にする例（Sales のPARealtimeTranscriptionClient）

**判断**:
- マニュアル側では **WSの既定を `127.0.0.1` として例示**し、`localhost` での接続失敗（IPv6 `::1`）が起こり得る点を補足する。

---

## CONFLICT-05: `/health` の「初期化完了」判定（実装依存）

- **Sales**
  - WS URL から HTTP Base を導出して `/health` をポーリングし、`status=healthy` に加えて `whisper.status=initialized` を待つ実装がある
  - 根拠: `manual/Dapp/d-sales/src/assets/js/voiceSettingsModal.js`（`pollUntilRealtimeHealthy()`）
- **OpenAPI**
  - `components/schemas/AudioHealth` の詳細と一致するかは要再確認（Dアプリ側が追加フィールドを見ている可能性）

**判断**:
- マニュアルでは **「Dアプリ実装での待ち条件」**として紹介し、レスポンスフィールドを仕様として断定しない。

---

## 更新履歴
- 2026-02-27: 初版作成（AudioNPUAPIの章リライトに伴う差分整理）

