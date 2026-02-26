## Dアプリ開発マニュアル 作成リスト（MECE・実装ベース）

### 適用範囲
- 対象アプリ: medical / retail / josys / sales
- 対象実装: `@Dapp/D-Josys/src` `@Dapp/d-medical/assets` `@Dapp/d-medical/map_pointer` `@Dapp/d-medical/record_summary` `@Dapp/d-medical/report_maker` `@Dapp/d-medical/resource` `@Dapp/d-retail/src` `@Dapp/D-sales/src`

---

## 分類（MECE境界）
- **Foundation**: Main/Preload/Build/Security（Electronのプロセス境界・配布設定・権限境界）
- **Renderer Common**: Renderer内の共通UI/ユーティリティ（ナビゲーション、モーダル、入力フォーカス補正、テンプレ等）
- **Persistence**: 保存（SQLite/KV/IndexedDB/localStorage）とファイル（Documentsフォルダ・ダイアログ）
- **Integrations**: 外部/ローカルHTTP・ストリーミング（IB-Link、chat/completions、search、StreamParser等）
- **AI Resources**: LLM/Voice の起動停止・ポリシー（ResourceManager）
- **Feature Modules**: 画面/機能単位（documents / role_playing / test_maker / map_pointer / record_summary / report_maker / shift_generator / multilingual_service / product_assistant 等）

---

## 作成対象ファイル一覧（章=1分類に所属）

### Foundation
- `10_Foundation_Electron_Bootstrap.md`
  - 対象実装:
    - `Dapp/D-Josys/src/index.js`
    - `Dapp/D-sales/src/index.js`
    - `Dapp/d-retail/src/main.js`
    - `Dapp/d-medical/main.js`
- `11_Foundation_Security_and_CSP.md`
  - 対象実装:
    - `Dapp/d-retail/src/main.js`（`webSecurity` 等）
    - `Dapp/d-medical/main.js`（`webSecurity`、permission）
    - `Dapp/d-retail/src/D-Retail/index.html`（CSP meta）
- `12_Foundation_Build_and_Packaging.md`
  - 対象実装:
    - 各 `package.json`（electron-builder設定）
    - `Dapp/d-retail/forge.config.js` / webpack config（存在する場合）
- `13_Foundation_Preload_Public_API.md`
  - 対象実装:
    - `Dapp/D-Josys/src/preload.js`
    - `Dapp/D-sales/src/preload.js`
    - `Dapp/d-retail/src/preload.js`
    - `Dapp/d-medical/preload.js`
- `14_Foundation_IPC_Channel_Catalog.md`
  - 対象実装:
    - `Dapp/D-Josys/src/index.js`（`ipcMain.handle(...)`）
    - `Dapp/D-sales/src/index.js`（`ipcMain.handle(...)`）
    - `Dapp/d-retail/src/main.js`（`ipcMain.handle(...)`）
    - `Dapp/d-medical/main.js`（`ipcMain.handle(...)`）

### Renderer Common
- `20_Renderer_Navigation_Shell.md`
  - 対象実装:
    - `Dapp/d-medical/assets/js/electronNavigation.js`
    - `Dapp/d-medical/common.js`（`window.electronAPI.navigateToPage` 呼び出し）
    - `Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.init.js`（`window.electronAPI.navigation.navigateToPage`）
- `21_Renderer_Modals_and_Alerts.md`
  - 対象実装（例）:
    - `Dapp/d-medical/record_summary/common.js`（共通モーダル呼び出し）
    - `Dapp/d-retail/src/D-Retail/multilingual_service/multilingual.init.js`（`showCommonModal`/`showCommonConfirmModal`）
- `22_Renderer_Focus_InputFix_System.md`
  - 対象実装:
    - `Dapp/d-medical/assets/js/electronNavigation.js`（`GlobalInputFocusManager` 連携）
    - `Dapp/d-medical/record_summary/common.js`
    - `Dapp/d-medical/report_maker/common.js`

### Persistence
- `30_Persistence_SQLite_KV.md`
  - 対象実装:
    - `Dapp/D-Josys/src/utils/KVDatabaseHelper.js`
    - `Dapp/D-sales/src/utils/KVDatabaseHelper.js`
    - `Dapp/d-retail/src/main.js`（SQLite生成/初期化）
- `31_Persistence_BrowserStorage.md`
  - 対象実装:
    - `Dapp/d-medical/map_pointer/utils.js`（`localStorage` / `chrome.storage.local`）
    - `Dapp/d-retail/src/D-Retail/shift_generator/assets/js/main.js`（`localStorage`→`IndexedDB` 移行）
- `32_Persistence_Files_and_DocumentsFolder.md`
  - 対象実装:
    - `Dapp/D-sales/src/index.js`（Documentsフォルダ `ensureFolder` 等）
    - `Dapp/d-retail/src/main.js`（ファイル選択/保存、documents系IPC）
- `33_Persistence_AppIdentity_and_Project.md`
  - 対象実装:
    - `Dapp/D-sales/src/utils/AppIdentityManager.js`
    - `Dapp/D-sales/src/utils/entities/ProjectManager.js`
    - `Dapp/D-Josys/src/utils/entities/ProjectManager.js`
    - `Dapp/D-Josys/src/preload.js` / `Dapp/D-sales/src/preload.js`（`projectAPI` 公開）

### Integrations
- `40_Integrations_IBLink_HTTP_and_Params.md`
  - 対象実装:
    - `Dapp/D-sales/src/api/IBLinkClient.js`
    - `Dapp/D-Josys/src/api/IBLinkClient.js`
    - `Dapp/d-retail/src/main.js`（`iblink:*` IPC）
    - `Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.rag.js`（HTTP/IPC併用）
- `41_Integrations_ChatCompletions_and_Streaming.md`
  - 対象実装:
    - `Dapp/D-Josys/src/assets/js/chat/ChatTransport.js`
    - `Dapp/D-Josys/src/assets/js/chat/StreamingQueueManager.js`
    - `Dapp/D-Josys/src/api/StreamParser.js`
    - `Dapp/D-sales/src/assets/js/apiClient.js`
- `42_Integrations_Search_RAG_Context.md`
  - 対象実装:
    - `Dapp/d-retail/src/D-Retail/product_assistant/product_assistant.services.rag.js`（検索→コンテキスト生成）
    - `Dapp/D-Josys/src/assets/js/apiClient.js`（検索/チャットの呼び出し）

### AI Resources
- `50_AIResources_LLM_ResourceManager.md`
  - 対象実装:
    - `Dapp/D-Josys/src/utils/LLMResourceManager.js`
    - `Dapp/D-sales/src/utils/LLMResourceManager.js`
    - `Dapp/d-retail/src/utils/LLMResourceManager.js`
    - `Dapp/d-medical/resource/LLMResourceManager.js`
- `51_AIResources_Voice_ResourceManager.md`
  - 対象実装:
    - `Dapp/D-Josys/src/utils/VoiceResourceManager.js`
    - `Dapp/D-sales/src/utils/VoiceResourceManager.js`
    - `Dapp/d-retail/src/utils/VoiceResourceManager.js`
    - `Dapp/d-medical/resource/VoiceResourceManager.js`

### Feature Modules（アプリ固有モジュールはここに集約）
- `60_Feature_Document_Management.md`
  - 対象実装:
    - `Dapp/D-Josys/src/document_management/**`
    - `Dapp/d-retail/src/D-Retail/document_management/**`
    - `Dapp/D-sales/src/documents/**`
- `61_Feature_Josys_TechSupportAI.md`
  - 対象実装:
    - `Dapp/D-Josys/src/tech_support_ai/**`
    - `Dapp/D-Josys/src/assets/js/chat/**`
- `62_Feature_Josys_WorkSupportAI.md`
  - 対象実装:
    - `Dapp/D-Josys/src/work_support_ai/**`
    - `Dapp/D-Josys/src/assets/js/voice/**`
- `63_Feature_Sales_RolePlaying.md`
  - 対象実装:
    - `Dapp/D-sales/src/role_playing/**`
- `64_Feature_TestMaker.md`
  - 対象実装:
    - `Dapp/D-sales/src/test_maker/**`
    - `Dapp/D-Josys/src/it_training_ai/**`
- `65_Feature_Retail_ShiftGenerator.md`
  - 対象実装:
    - `Dapp/d-retail/src/D-Retail/shift_generator/**`
- `66_Feature_Retail_MultilingualService.md`
  - 対象実装:
    - `Dapp/d-retail/src/D-Retail/multilingual_service/**`
- `67_Feature_Retail_ProductAssistant.md`
  - 対象実装:
    - `Dapp/d-retail/src/D-Retail/product_assistant/**`
- `68_Feature_Medical_MapPointer.md`
  - 対象実装:
    - `Dapp/d-medical/map_pointer/**`
- `69_Feature_Medical_RecordSummary.md`
  - 対象実装:
    - `Dapp/d-medical/record_summary/**`
- `70_Feature_Medical_ReportMaker.md`
  - 対象実装:
    - `Dapp/d-medical/report_maker/**`
- `71_Feature_Screenshot_Shot.md`
  - 対象実装:
    - `Dapp/D-Josys/src/preload.js` / `Dapp/D-Josys/src/index.js`
    - `Dapp/d-retail/src/preload.js` / `Dapp/d-retail/src/main.js`

---

## 差分/競合（存在する場合）
- 競合ログ: `90_Conflict_Log.md`
- 優先順位: medical > retail > josys > sales

