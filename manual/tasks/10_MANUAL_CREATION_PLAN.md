## Dアプリ開発マニュアル 作成計画（medical > retail > josys > sales）

### 目的（事実）
- 本計画は、`MD/dapp-manual/` 配下にマニュアル群を出力する手順を定義する

### 成果物の配置（固定）
- **作業計画（このファイル）**: `tasks/dapp-manual/10_MANUAL_CREATION_PLAN.md`
- **マニュアル本体（= @MD）**: `MD/dapp-manual/`
  - 入口: `00_Index.md`
  - 作成リスト（MECE）: `01_Manual_List.md`
  - 競合ログ: `90_Conflict_Log.md`
  - テンプレ: `_TEMPLATE_SIMPLE.md`
  - そのほかのマニュアル: `01_Manual_List.md` の「作成対象ファイル一覧」に従う

---

## 作成フロー（全マニュアル共通）

### 1) 事実収集（必須）
- 参照順は固定: **medical → retail → josys → sales**
- 各アプリについて「現状の挙動/設定/制約」を箇条書きで抜く（推測しない）

### 2) 競合検出（必須）
- 同じ概念で **保存先・命名・API・セキュリティ・戻り値形式** がズレていたら競合
- 競合は本文に散らさない（詳細は競合ログへ）。

### 3) 競合の記録と決定（必須）
- `MD/dapp-manual/90_Conflict_Log.md` に **CONFLICT-YYYYMMDD-XX** を起票
- 決定の原則は固定: **medical > retail > josys > sales**
- 例外は「セキュリティ/法令/運用破綻（書き込み不可等）」のみ。例外を使う場合は理由をログに残す。

### 4) マニュアル本文の作成（必須）
- `MD/dapp-manual/_TEMPLATE_SIMPLE.md` を複製し、各マニュアルを作成する
- 記載は **事実のみ**（主観・推奨・チェックリスト・MUST等の規範文は書かない）

### 5) レビュー（必須）
- **MECE**: `MD/dapp-manual/01_Manual_List.md` の分類（Foundation / Renderer Common / Persistence / Integrations / AI Resources / Feature Modules）のうち、どれか1つにのみ所属させる
- **競合漏れ**: “各アプリの現状”の差分がログに起票されているか
- **運用性**: 新規Dアプリがこの章だけ読んで実装判断できるか

---

## 出力順（依存関係つき）
> 入口と競合ログを先に用意し、その後に各論を出力する。

### Phase 0: 置き場/入口（当日）
- `MD/dapp-manual/00_Index.md`（入口）
- `MD/dapp-manual/01_Manual_List.md`（作成リスト=MECE境界）
- `MD/dapp-manual/90_Conflict_Log.md`（競合ログ）
- `MD/dapp-manual/_TEMPLATE_SIMPLE.md`（テンプレ）

### Phase 1: Foundation
- `10_Foundation_Electron_Bootstrap.md`
- `11_Foundation_Security_and_CSP.md`
- `12_Foundation_Build_and_Packaging.md`
- `13_Foundation_Preload_Public_API.md`
- `14_Foundation_IPC_Channel_Catalog.md`

### Phase 2: Renderer Common
- `20_Renderer_Navigation_Shell.md`
- `21_Renderer_Modals_and_Alerts.md`
- `22_Renderer_Focus_InputFix_System.md`

### Phase 3: Persistence
- `30_Persistence_SQLite_KV.md`
- `31_Persistence_BrowserStorage.md`
- `32_Persistence_Files_and_DocumentsFolder.md`
- `33_Persistence_AppIdentity_and_Project.md`

### Phase 4: Integrations
- `40_Integrations_IBLink_HTTP_and_Params.md`
- `41_Integrations_ChatCompletions_and_Streaming.md`
- `42_Integrations_Search_RAG_Context.md`

### Phase 5: AI Resources
- `50_AIResources_LLM_ResourceManager.md`
- `51_AIResources_Voice_ResourceManager.md`

### Phase 6: Feature Modules
- `60_Feature_Document_Management.md`
- `61_Feature_Josys_TechSupportAI.md`
- `62_Feature_Josys_WorkSupportAI.md`
- `63_Feature_Sales_RolePlaying.md`
- `64_Feature_TestMaker.md`
- `65_Feature_Retail_ShiftGenerator.md`
- `66_Feature_Retail_MultilingualService.md`
- `67_Feature_Retail_ProductAssistant.md`
- `68_Feature_Medical_MapPointer.md`
- `69_Feature_Medical_RecordSummary.md`
- `70_Feature_Medical_ReportMaker.md`
- `71_Feature_Screenshot_Shot.md`

---

## 各章で「必ず競合チェックする観点」（抜け防止）
- **保存先**: userData / installDir / home配下（書き込み権限の破綻がないか）
- **DB方式**: better-sqlite3 / sqlite3、seedコピー/初回クリーン、スキーマ命名（snake/camel）
- **IPC**: チャンネル命名、戻り値 `{success,data,error}` の揃え、権限境界（許可パス）
- **セキュリティ**: `webSecurity`、外部URL、CSP、権限自動許可の可否
- **IB-Link**: `/documents/process` と `/documents/search` のパラメータ差異（directories/limit等）
- **LLM/音声**: startedByApp 安全弁、stopOnQuit、autoStart、localhost縛り
- **配布**: `asarUnpack`、`extraResources`、アイコン、アンインストール時データ削除

