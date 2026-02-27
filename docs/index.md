# IB-Link 操作マニュアル


IB-Link 操作マニュアル
## 更新履歴
2026/02/13 推奨モデル追記  
2026/01/29 バージョン4.0対応  
2025/12/12 モデル切り替えAPI追記  
2025/11/21 モデル操作修正  
2025/11/17 Document API利用フロー追記およびRuntime設定修正  
2025/11/11 Chat APIおよび補足追記  
2025/09/30 バージョン3.0対応  
2025/09/09 バージョン2.0対応  
2025/07/15 「IB-Link」表記修正  
2025/06/25 「利⽤者向け機能」「開発者向け機能」章分け  
2025/06/18  初版  

## ⽬次

1. システム概要
2. 機能概要
3. 利⽤者向け機能  
   3.1. モデル操作  
   3.2. モデル選択と起動⼿順  
   3.3. マルチモーダルモデル  
   3.4. IB-Link 停⽌⼿順  
   3.5. 初期化失敗時の再イニシャライズ（再実行）  
4. 開発者向け機能  
   4.1. チャットの使い⽅  
   4.2. Runtime（ランタイム）設定  
   4.3. Logs機能  
   4.4. ドキュメント埋め込み  
   4.5. Chat API  
   4.6. Documents API  
   4.7. Retriever API
   4.8. Audio API  
   4.9. モデル切り替え API  
## 1.システム概要
   ⼤規模⾔語モデル（LLM）をPC上で実⾏・実験できるLLM利⽤アプリケーションです。
## 2.機能概要
   利⽤者向け機能と開発者向け機能が⽤意されています。
   利⽤者向け機能 （D-アプリをご利⽤いただくための機能になります。）
   モデル操作
   起動・停⽌ （OS起動時に⾃動でIB-Linkは起動され利⽤可能状態になります。）
   開発者向け機能
   チャット
   Runtime(ランタイム)設定
   ログ操作
   ドキュメント埋め込み機能
   ⾳声⽂字起こし
   データベース
   API



## 3.利⽤者向け機能
### 3.1 モデル操作
#### 3.1.1 GGUF形式のLLMモデル操作
「Models」タブでは、利⽤するGGUF形式のLLMモデルを検索・選択・ダウンロードできます。
初期状態 デフォルトのモデルが選択され、使⽤可能な状態になっています。
最適なモデル選定 速度重視の軽量モデル／精度重視の⼤型モデルを簡単に切り替え、⽤途に合った
LLMを試せます。
モデルバージョン管理 旧版も併存させて⽐較しながら検証できるので、アップグレード判定がスムー
ズ。

1. 「GGUF Models」タブをクリックすると、モデル管理画⾯が表⽰されます。
   右側にモデルの詳細情報が表⽰されます。
   モデルは C:\Users\<ユーザー名>\.iblink\Models に保存されます。


![図: 画像 1](images/page-003_img-001.png)



---



2. モデルを検索する  
   上部の検索バーにモデル名を⼊⼒すると、該当する候補が⼀覧に表⽰されます。
   例︓Qwen3-0.6B と⼊⼒すると、該当するGGUFモデルがリストに出てきます。
   絞り込み可能です（部分⼀致）。


![図: 画像 1](images/page-004_img-001.png)



---



3. 任意のモデルをクリックすると、右側にモデル情報が表⽰されます。
   作成者、種類、ファイルサイズ、作成⽇、最終更新⽇などが確認可能です。
   複数のGGUFファイルがある場合、それぞれ選択できます。


![図: 画像 1](images/page-005_img-001.png)



---



4. 「Available GGUF Files」からダウンロードするファイルを選び、「Download Selected File」ボタンをクリックします。
   ダウンロードの進捗が画⾯下に表⽰されます（例︓10.9%）。
   複数ファイルがある場合は、任意の精度（例︓q5_k, q8_0など）を選択できます。


![図: 画像 1](images/page-006_img-001.png)



---



5. ダウンロード完了メッセージ  
   ダウンロードが完了すると、Donwloaded Modelsにモデルが表示されます。
   保存先︓C:\Users\<ユーザー名>\.iblink\Models
   チャット画⾯でモデルが使⽤可能になります。


![図: 画像 1](images/page-007_img-001.png)



---



6. モデルの削除は、「Donwloaded Models」の削除対象のモデルを選択し、「Delete」をクリックします。


![図: 画像 1](images/page-007_img-002.png)

  OKをクリックすると削除されます。

![図: 画像 1](images/page-007_img-003.png)


---
#### 3.1.2 Foundry LocalのLLMモデル操作　（Intel版は本機能がございません）
1. FL Modelsタブを開く  
   「Reflesh Models」をクリックすると、Available Modelsにモデルが表示されます。ダウンロードするモデルを選択し、「Download Model」をクリックします。  


![図: 画像 1](images/page-007_img-004.png)

2. モデルのダウンロード開始  
　 
![図: 画像 1](images/page-007_img-005.png)

3. ダウンロードが完了すると、右の「Download Models」に表示されます。

![図: 画像 1](images/page-007_img-006.png)

4. モデルの削除は、「Download Models」に表示されているモデルから対象を選択します。

![図: 画像 1](images/page-007_img-007.png)

5. 「Delete Models」をクリックします。 
![図: 画像 1](images/page-007_img-008.png)

---
#### 3.1.3 推奨モデル（Intel版）
Intel版で利用できる推奨モデルを以下に示します。

##### 1. unsloth/Qwen3-VL-2B-Instruct-1M-GGUF ※マルチモーダル
画像とテキストの両方を理解できるマルチモーダルモデルです。  

**推奨ファイル:**
- モデル: `Qwen3-VL-2B-Instruct-1M-UD-Q5_K_XL.gguf`
- Visionエンコーダー: `mmproj-F16.gguf`

##### 2. unsloth/Qwen3-VL-2B-Thinking-1M-GGUF
思考プロセスを重視したモデルです。複雑な推論タスクに適しています。

**推奨ファイル:**
- モデル: `Qwen3-VL-2B-Thinking-1M-UD-Q5_K_XL.gguf`

##### 3. LiquidAI/LFM2.5-1.2B-JP-GGUF
日本語に特化した軽量モデルです。日本語タスクで高い性能を発揮します。

**推奨ファイル:**
- モデル: `LFM2.5-1.2B-JP-Q6_K.gguf`

##### 4. mradermacher/shisa-v2.1-lfm2-1.2b-GGUF
日本語と英語の両方に対応したモデルです。

**推奨ファイル:**
- モデル: `shisa-v2.1-lfm2-1.2b.Q6_K.gguf`

##### 5. unsloth/Qwen3-4B-Instruct-2507-GGUF
汎用的な指示実行タスクに適した4Bパラメータモデルです。

**推奨ファイル:**
- モデル: `Qwen3-4B-Instruct-2507-UD-Q4_K_XL.gguf`

---

#### 3.1.4 推奨モデル（Qualcomm版）
Qualcomm版で利用できる推奨モデルを以下に示します。

##### 1. unsloth/Qwen3-0.6B-GGUF     
軽量で扱いやすいモデルです。高精度な量子化で性能を保ちます。

**推奨ファイル:**
- モデル: `Qwen3-0.6B-UD-Q8_K_XL.gguf`

##### 2. ggml-org/gemma-3-4b-it-qat-gguf ※マルチモーダル   
画像とテキストの両方を理解できるマルチモーダルモデルです。 

**推奨ファイル:**
- モデル: `gemma-3-4b-it-qat-Q4_0.gguf`
- Visionエンコーダー: `mmproj-model-f16-4B.gguf`

---
### 3.2 モデル選択と起動⼿順
ダウンロード済みのモデルを選択し、起動するための⼿順を解説します。

1. 現在のモデル確認とチャット初期状態
   IB-Linkが起動し、チャット画⾯でモデルが表⽰されている状態。
   右上のStop Serverをクリックするとサーバが停⽌します。
   Statusが Server stopped になれば停⽌状態になります。


![図: 画像 1](images/page-008_img-001.png)



---



2. サーバー停⽌後の状態
   StatusがServer stopped の場合は機能しません。
   モデルは選択済みでも、サーバーを起動しなければ使⽤できません。


![図: 画像 1](images/page-009_img-001.png)



---



3. モデル選択⼿順  
   画⾯上部の Model: ドロップダウンをクリックし、使⽤したいモデル（例︓Qwenやtinyswallow）を選びま
   す。
   .gguf 形式のモデルファイルから選べます。


![図: 画像 1](images/page-010_img-001.png)



---



4. サーバーを起動していないと以下のような警告が表⽰されます。  
   To start chatting, either:
   Run the local server (click 'Run Server' button)
   Configure OpenAI API settings in the Runtime tab


![図: 画像 1](images/page-011_img-001.png)



---



5. サーバーを起動する  
   右上の Run Server ボタンをクリックすると、ローカルモデルのロードが始まります。
   ステータス︓Loading model... → Server running になると起動完了になります。


![図: 画像 1](images/page-012_img-001.png)



---



### 3.3 マルチモーダルモデル
マルチモーダルモデルを使⽤する⼿順を記載します。  

1. Models でモデルを検索
   左側サイドバーで Models を開き、検索ボックスに次を⼊⼒します。
   ggml-org/gemma-3-4b-it-qat-gguf
2. リポジトリを選択して内容を確認  
   検索結果から ggml-org/gemma-3-4b-it-gguf を選択します。右側の Model Information に基本情報と利⽤可能な GGUF ファイルが表⽰されます。  
   Available GGUF Files に以下の 2 つが⾒えることを確認します。
   gemma-3-4b-it-qat-Q4_0.gguf（約 2.35GB）
   mmproj-model-f16-4B.gguf（約 0.79GB）


![図: 画像 1](images/page-013_img-001.png)



---



3. Gemma 本体（Q4_0）をダウンロード  
   gemma-3-4b-it-qat-Q4_0.gguf を選択し、右下の Download Selected GGUF File をクリック。進捗が下部に表⽰されます。  
   ダウンロード完了メッセージが出るまで待ちます。


![図: 画像 1](images/page-014_img-001.png)


![図: 画像 2](images/page-014_img-002.png)



---



4. mmproj（投影モデル）をダウンロード  
   続けて mmproj-model-f16-4B.gguf を選択して同様にダウンロードします。
   完了を確認します。


![図: 画像 1](images/page-015_img-001.png)


![図: 画像 2](images/page-015_img-002.png)



---



5. ローカルサーバーを停⽌  
   左側サイドバーで Chat を開きます。 右上の Stop Server をクリックしてサーバーを起動します。ステータスが Server stopped になることを確認します。  
   上部の Model ドロップダウンから gemma-3-4b-it-qat-Q4_0.gguf を選択します。  
   <>アイコンを押下して、詳細設定ページを開きます。
   Custom Arguments に mmproj を追加します︓


![図: 画像 1](images/page-016_img-001.png)


![図: 画像 2](images/page-016_img-002.png)



---



追加ボタン（Add Custom Argument）を押し、名前に --mmproj、値に C:\Users\<ユーザー名

>\.iblink\Modelsmmproj-model-f16-4B.gguf を⼊⼒
>（モデルと同じディレクトリにある前提・相対指定が可能です）
>Save Setting をクリック
>プレビュー（Command Preview）に --mmproj "mmproj-model-f16-4B.gguf" が含まれていることを確認します。  

6. ローカルサーバーを起動
   右上の Run Server をクリックしてサーバーを起動します。ステータスが Server running になったら、下部
   の⼊⼒欄からチャットを開始できます。
7. D-Appを再起動してください。
   うまくいかないときは、モデルが⾒つからない/読み込めないDownload Location（…\.iblink\Models）にファイルがあるか確認します。  
   モデル名の拡張⼦が .gguf で⼀致しているか確認します。  
   mmproj が効いていない  
   Custom Arguments に --mmproj mmproj-model-f16-4B.gguf が⼊っているか、Command Preview に反映されているか確認します。  


![図: 画像 1](images/page-017_img-001.png)



---



### 3.4 IB-Link 停⽌⼿順

1. IB-Linkが起動中であることを確認  
   IB-Link の画⾯右上にある Status: Server running を確認します。
2. 「Stop Server」ボタンをクリック  
   上部の「Stop Server」ボタンをクリックして、ローカルサーバを停⽌します。


![図: 画像 1](images/page-018_img-001.png)



---



3. IB-Link停⽌を確認  
   「Status」が Server stopped に変わっていることを確認します。  
4. タスクトレイから IB-Link を終了（必要に応じて）  
   タスクバーのトレイアイコンから IB-Link を右クリックし、Exit を選択します。  


![図: 画像 1](images/page-019_img-001.png)


![図: 画像 2](images/page-019_img-002.png)





### 3.5 初期化失敗時の再イニシャライズ（再実行）

初回起動（初期化：IB-Link Setup）が途中で失敗した場合、失敗したステップのみを選択して再実行（再イニシャライズ）できます。

#### 3.5.1 事前確認

- IB-Link を起動し、左メニューの `Setup` を開きます。
- 画面下部の `Activity Log` に失敗理由（例：ネットワークエラー、依存関係の導入失敗など）が表示されている場合は、先に内容を確認します。

#### 3.5.2 ネットワークエラー（Prerequisites）が出る場合

依存コンポーネント（例：Visual C++ Redistributable）の取得でネットワークが必要になる場合があります。

1. `Network Connection Required` の警告が表示されたら、ネットワーク接続を確認します。
2. 右側の `Retry` をクリックして再試行します。
3. 繰り返し失敗する場合は、警告内に表示されるダウンロード URL から手動導入し、再度 `Retry` をクリックします。

![図: ネットワーク接続が必要](images/page-040_img-060.png)

#### 3.5.3 再イニシャライズ（再実行）の実施

1. 左メニューから `Setup` を開き、`Initialization Complete`（または Setup 画面）まで進んでいることを確認します。
2. `Re-run Initialization Steps` で、再実行したいステップにチェックを入れます。
3. `Re-initialize Selected` をクリックして再実行します。

![図: 再実行ステップ選択（全体）](images/page-040_img-061.png)

##### 3.5.3.1 Prerequisites（前提条件）を再実行する例

1. `Prerequisites` にチェックを入れます。
2. `Re-initialize Selected` をクリックします。

![図: Prerequisites を選択](images/page-040_img-062.png)

実行中はステップが `In Progress` になり、進捗とログが更新されます。

![図: Prerequisites 再実行中](images/page-040_img-063.png)

完了すると当該ステップが `Done`（緑のチェック）になります。

![図: Prerequisites 完了](images/page-040_img-064.png)

##### 3.5.3.2 Whisper を再実行する例

1. `Whisper` にチェックを入れます。
2. `Re-initialize Selected` をクリックします。

![図: Whisper を選択](images/page-040_img-065.png)

実行中は `Whisper Setup` が `In Progress` になり、進捗が表示されます。

![図: Whisper 再実行中](images/page-040_img-066.png)

完了すると `Whisper` が `Done` になります。

![図: Whisper 完了](images/page-040_img-067.png)

##### 3.5.3.3 Models（Chat Model）を再実行する例

1. `Models` にチェックを入れます。
2. `Re-initialize Selected` をクリックします。

![図: Models を選択](images/page-040_img-068.png)

実行中はダウンロード進捗とログが表示されます。

![図: Models 再実行中](images/page-040_img-069.png)

完了すると `Models` が `Done` になります。

![図: Models 完了](images/page-040_img-070.png)

#### 3.5.4 再実行がうまくいかない場合の確認ポイント

- **ログ確認**: `Setup` 画面の `Activity Log` を確認し、失敗要因（ネットワーク、権限、容量、依存導入など）を切り分けます。  
  例：`C:\Users\<ユーザー名>\.iblink\logs\initialization_*.log`
- **ネットワーク**: 企業プロキシ／FW 環境では外部取得がブロックされることがあります。必要に応じて手動導入後に再実行します。
- **権限**: 依存導入で管理者権限が必要になることがあります。
- **ディスク容量**: `Models` 再実行はモデル取得で容量が必要です。

## 4. 開発者向け機能
### 4.1 チャットの使い⽅
5. チャットの新規作成
   左上の New Chat ボタンをクリックすると、新しい会話が作成されます。


![図: 画像 1](images/page-020_img-001.png)



---



2. メッセージの⼊⼒と送信  
   下部のテキストボックスにメッセージを⼊⼒し、右側の⻘い⽮印ボタンをクリックして送信します。  


![図: 画像 1](images/page-021_img-001.png)



---



3. 応答の確認
   アシスタントの返信が緑⾊の背景で表⽰されます。


![図: 画像 1](images/page-022_img-001.png)



---



### 4.2 Runtime 設定
Runtime タブでは、ローカルモデルの実⾏に必要な Llamaサーバー設定 と API設定 を構成できます。
初期状態 デフォルトの Llama が選択され、使⽤可能な状態になっています。
ハードウェアに合わせた最適化 ⾃PCの命令セットに合う Llama バイナリを選ぶことで推論速度を最⼤化できます。 
なお、Embedding APIは機能としては提供しておりません。 

1. Llama Server 設定タブ
   ローカル実⾏⽤ Llama サーバーの .exe 実⾏パスを指定し、任意のバージョンを選択またはダウンロードできます。  
2. 操作⼿順
3. llama-server.exe を指定
   Browse ボタンで任意のバイナリファイルを選択
4. Select from Downloaded Servers から⾃動抽出されたバージョンを選択するとそのパスが有効になります。  
5. 必要に応じて Release Tag と Zip File Name を⼊⼒し、モデルをダウンロードします。  
   例: b5085, llama-b5085-bin-win-avx2-x64


![図: 画像 1](images/page-023_img-001.png)



---



### 4.3 Logs機能
Server Logs の確認  
上部タブから Server Logs を選択します。
アプリ起動時の状態、モデルロード、OCR設定、バックグラウンドサービスの状態などが時系列で表⽰されます。  
例: APIキーの読込、ローカルサーバの起動、OCR対象ディレクトリ数、エラー/警告 等。
API Logs の確認  
上部タブから API Logs を選択します。すべてのAPIログを⼀覧で確認できます。  


![図: 画像 1](images/page-025_img-001.png)


![図: 画像 2](images/page-025_img-002.png)



---



API の絞り込み（Filter API）

1. 画⾯上部の Filter API ドロップダウンをクリックします。
2. All / Documents API / Embeddings API / Retriever API / Audio API などから対象を選択します。
   Documents API のログを⾒る  
   Documents API を選択すると、ドキュメント処理（OCR、分割、チャンク数、進捗％、成功/失敗件数、ストレージ使⽤量など）の詳細が確認できます。  
   例:「Processed file」「Strategy: Sync」「Chunks」「Progress」「Succeeded/Failed」 などの⾏で処理結果を確認できます。  


![図: 画像 1](images/page-026_img-001.png)


![図: 画像 2](images/page-026_img-002.png)



---



OCR=True/False、分割戦略、チャンク数、実⾏時間、リソース使⽤量
（Storage/DB/Embeddings/Processing）等
Embeddings API のログを⾒る
Embeddings API を選択すると、トークン化、推論時間、バッチサイズ、メモリ使⽤量、⽣成された
埋め込み数などが確認できます。
Retriever API のログを⾒る
Retriever API を選択すると、問い合わせテキストに対する埋め込み⽣成、RDBクエリ（例: SELECT
COUNT(*) FROM "DocumentEmbeddings"）実⾏、応答時間（ms）などが確認できます。
共通操作（⾃動スクロール・差分のみ・保存/クリア）


![図: 画像 1](images/page-027_img-001.png)


![図: 画像 2](images/page-027_img-002.png)



---



Auto-scroll: 新しいログが出ると⾃動で末尾へ追従します。⻑時間の監視に便利です。
Changes Only: 変化のある⾏だけを表⽰してノイズを減らします。
Status: 現在の稼働状態（例: Running (Healthy) (Standalone)）が表⽰されます。
Refresh: 表⽰を更新します。
Save Logs: 現在の表⽰内容をファイルに保存します（監査・共有⽤）。
Clear Logs: 画⾯上のログ表⽰をクリアします（※サーバ側のログ消去とは異なる場合があります）。
Start/Stop/Restart API: 埋め込みやリトリーバー等のAPIサービスの起動/停⽌/再起動を⾏います（権
限・構成に依存）。
トラブルシューティングのヒント
エラーが出た時刻を基点に Server Logs と API Logs を併読し、原因箇所（起動直後・ドキュメント処理・埋め込み⽣成・検索処理など）を切り分けます。
Filter API で対象を絞り、Changes Only をオンにして差分だけを追うと効率的です。



---



### 4.4 ドキュメント埋め込み

1. 画⾯を開く
2. IB-Link を起動し、左メニューから Embedding を開く。
3. ルートフォルダを選択
4. 左 Document Library の Root Directory で Browse… をクリックし、埋め込み対象フォルダを選択。
5. ツリーに出たファイルへチェック（Select All でも可）。
6. スキャンPDFはツリー上部の OCR を有効化。
7. 埋め込み処理の開始


![図: 画像 1](images/page-029_img-001.png)


![図: 画像 2](images/page-029_img-002.png)



---



1. Process をクリックして埋め込み開始。
2. 進捗は下部 Embedding Progress に表⽰。
3. 処理完了の確認
4. 「Processing Complete」ダイアログが出たら OK。
5. Documents to embed が 100% で、Completed Files に並んでいることを確認。
   「Files processed: 0 (no new files needed processing)」は差分なし／対象外の意味。更新やOCR
   設定、選択状態を確認。


![図: 画像 1](images/page-030_img-001.png)


![図: 画像 2](images/page-030_img-002.png)



---



5. 埋め込み済みドキュメントの選択
6. 右 Embedded Documents で Refresh。
7. 使いたいドキュメントにチェック（Select All も可）。不要なら Delete Selected。
8. チャットで質問（検索）
9. 上部 Chat に移動。


![図: 画像 1](images/page-031_img-001.png)


![図: 画像 2](images/page-031_img-002.png)



---



2. 右で選択したドキュメントを根拠に回答されるので、質問を⼊⼒して送信。


![図: 画像 1](images/page-032_img-001.png)



---
### 4.5 イニシャライズ・データベースセットアップ

概要
イニシャライズ状態を確認し、PostgreSQL の接続設定（Database Connection Setup）を行って、接続テスト成功までを確認する。


---

1. 左メニューから **Setup** を開く。
2. 画面上部のセットアップステップがすべて **Done** になっていることを確認する。  
   - Prerequisites / Database / App Setup / Whisper / Models / Finalize
3. **Initialization Complete** が表示され、進捗が **100%** になっていることを確認する。

![IB-Link Setup 完了画面](images/page-033_img-001.png)

---

#### 4.5.1 再イニシャライズ（必要な場合のみ）

「3.5 初期化失敗時の再イニシャライズ」を参照してください。

---

#### 4.5.2 Database Settings（タイムゾーン設定）

1. **Database Settings** の **Time Zone Settings** でタイムゾーンを選択する。  
   - 例：`Asia/Tokyo`
2. **Apply** をクリックして反映する。

![Time Zone Settings](images/page-033_img-001.png)

---

#### 4.5.3 Database Connection Setup（接続設定）

1. **Database Actions** の **Setup / Fix Database Connection** をクリックする。
2. **Database Connection Setup** 画面が表示されることを確認する。

![Database Connection Setup（入力前）](images/page-033_img-002.png)

3. 接続情報を入力する
以下の項目を入力する（画像の例）：

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `iblink_wada_masanori`
- **Username**: `postgres`
- **Password**: （PostgreSQL のパスワード）

![Database Connection Setup（入力中）](images/page-033_img-003.png)

4. 接続テストを実行する
5. **Test Connection** をクリックする。
6. 画面下部に **「Connection successful! Server is reachable.」** と表示されることを確認する。

![Connection successful 表示](images/page-033_img-004.png)

#### 4.5.4 DBセットアップを実行する（必要な場合）
- 接続テスト成功後、DB作成／初期化が必要な運用の場合は **Setup Database** をクリックする。  
  ※既存DBに接続するだけの運用では不要な場合があります。

---

#### 4.5.5 診断（任意）
- **Database Actions** の **Run Diagnostics** をクリックすると、診断結果が表示される。
- 画面上で **Connected to PostgreSQL database**（接続済み）表示を確認する。

![Diagnostics / Connected 表示](images/page-033_img-001.png)


---


### 4.6 DocumentsAPI
概要  
DocumentsAPI は、IB-Link（Documents サービス）に対して **ドキュメント取り込み（非同期）/状態取得/検索/抽出/一覧/削除** を行う HTTP API です。

---

#### Base URL
- `http://localhost:8500/iblink/v1`
  - `http://localhost:8500/iblink` を base にして `/v1/documents/...` を組み立てる構成もあります。

---

#### 共通
- Headers
  - `Content-Type: application/json`（`charset=utf-8` を付ける場合があります）

---

#### Endpoints
- 取り込み（非同期）: POST `/documents/process`
- 状態取得: POST `/documents/status`
- 検索: POST `/documents/search`
- 抽出（埋め込み生成なし）: POST `/documents/extract`
- 一覧: POST `/documents/list`
- 削除: DELETE `/documents/delete`
- 情報: GET `/documents/info`
- ヘルス: GET `/documents/health`

補足
- 本節は **`http://localhost:8500/iblink/v1` 配下の `/documents/*`** を扱います。
- DocumentsAPI（`POST /documents/search`）と RetrieverAPI（`POST /retriever`）は **別系統**です（Base URL が異なり、レスポンス形状も異なります）。

---

#### 代表フロー
1. **取り込み**（POST `/documents/process`）でジョブ作成 → `job_id` を受け取る
2. **進捗/完了確認**（POST `/documents/status`）を `status_type: "processing"` でポーリングする
3. **検索**（POST `/documents/search`）で取り込み済みコンテンツを参照する
4. **削除**（DELETE `/documents/delete`）で対象を消す（必要に応じてファイル側も削除する）

---

#### Request / Response

1) 取り込み（非同期）: POST `/documents/process`  
必須: `files` または `directories`, `d_app_id`, `project_id`  
補足: `files` の要素は「文字列パス」または `{ file_path, enable_ocr }` を指定できます。  

```json
{
  "d_app_id": "my-app",
  "project_id": "project-001",
  "duplicate_strategy": "sync",
  "files": [
    { "file_path": "C:\\Documents\\report.pdf", "enable_ocr": false },
    { "file_path": "C:\\Scans\\receipt.png", "enable_ocr": true }
  ]
}
```

呼び出し例

```bash
curl -X POST http://localhost:8500/iblink/v1/documents/process \
  -H "Content-Type: application/json" \
  -d '{"files":["C:\\Documents\\report.pdf"],"d_app_id":"my-app","project_id":"project-001"}'
```

レスポンス（例: 202）

```json
{
  "job_id": "my-app_project-001_20250120_103000",
  "status": "pending",
  "status_url": "/iblink/v1/documents/status"
}
```

2) 状態取得: POST `/documents/status`  
（`status_type: "processing"` の例）送信フィールド: `status_type`, `job_id`, `include_files`, `d_app_id`, `project_id`  

```json
{
  "status_type": "processing",
  "d_app_id": "my-app",
  "project_id": "project-001",
  "job_id": "my-app_project-001_20250120_103000",
  "include_files": true
}
```

呼び出し例

```bash
curl -X POST http://localhost:8500/iblink/v1/documents/status \
  -H "Content-Type: application/json" \
  -d '{"status_type":"processing","d_app_id":"my-app","project_id":"project-001","job_id":"my-app_project-001_20250120_103000","include_files":true}'
```

`status_type`
- `processing`: ジョブ進捗
- `queue`: キュー状態
- `quota`: 使用量
- `health`: ヘルス
- `dependency`: 依存状態
- `jobs`: ジョブ一覧

3) 検索: POST `/documents/search`  
送信フィールド（例）: `query`, `d_app_id`, `project_id`  

```json
{
  "query": "検索クエリ",
  "d_app_id": "my-app",
  "project_id": "project-001",
  "limit": 5,
  "directories": ["C:\\Documents\\manuals"],
  "document_ids": ["550e8400-e29b-41d4-a716-446655440000"],
  "similarity_threshold": 0.7,
  "search_mode": "hybrid"
}
```

呼び出し例

```bash
curl -X POST http://localhost:8500/iblink/v1/documents/search \
  -H "Content-Type: application/json" \
  -d '{"query":"検索クエリ","d_app_id":"my-app","project_id":"project-001"}'
```

補足
- 任意: `limit` / `directories` / `document_ids` / `similarity_threshold` / `search_mode` を指定します。
- 入力キーとして `text` を受け取る場合は、送信前に `query` へ正規化します。

4) 削除: DELETE `/documents/delete`  
送信フィールド（例）: `d_app_id`, `project_id`, `file_paths`, `delete_all`  

```json
{
  "d_app_id": "my-app",
  "project_id": "project-001",
  "file_paths": ["C:\\Documents\\old-doc.pdf"],
  "delete_all": false
}
```

呼び出し例

```bash
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{"d_app_id":"my-app","project_id":"project-001","file_paths":["C:\\Documents\\old-doc.pdf"]}'
```

プロジェクト全削除（`delete_all`）

```bash
curl -X DELETE http://localhost:8500/iblink/v1/documents/delete \
  -H "Content-Type: application/json" \
  -d '{"d_app_id":"my-app","project_id":"project-001","delete_all":true}'
```

5) 抽出（埋め込み生成なし）: POST `/documents/extract`
送信フィールド（例）: `files`, `d_app_id`, `project_id`, `include_metadata`

```json
{
  "d_app_id": "my-app",
  "project_id": "project-001",
  "files": ["C:\\Documents\\report.pdf"],
  "include_metadata": true
}
```

呼び出し例

```bash
curl -X POST http://localhost:8500/iblink/v1/documents/extract \
  -H "Content-Type: application/json" \
  -d '{"files":["C:\\Documents\\report.pdf"],"d_app_id":"my-app","project_id":"project-001"}'
```

6) 一覧: POST `/documents/list`
送信フィールド（例）: `list_type`, `d_app_id`, `project_id`, `file_extension`

```json
{
  "list_type": "documents",
  "d_app_id": "my-app",
  "project_id": "project-001",
  "file_extension": ".pdf"
}
```

呼び出し例

```bash
curl -X POST http://localhost:8500/iblink/v1/documents/list \
  -H "Content-Type: application/json" \
  -d '{"list_type":"documents","d_app_id":"my-app","project_id":"project-001"}'
```

7) 情報: GET `/documents/info`

```bash
curl http://localhost:8500/iblink/v1/documents/info
```

8) ヘルス: GET `/documents/health`

```bash
curl http://localhost:8500/iblink/v1/documents/health
```

---

### 4.7 RetrieverAPI
概要  
RetrieverAPI は、取り込み済みドキュメント（チャンク）に対して **ベクトル検索/ハイブリッド検索** を実行し、該当チャンク（`results[]`）を返すHTTP APIです。

---

#### Base URL
- `http://localhost:6500/iblink/v1`

---

#### 共通
- Headers
  - `Content-Type: application/json`（JSON body を送るPOSTのみ）

---

#### Endpoints
- 検索: POST `/retriever`
- ヘルス: GET `/retriever/health`
- 情報: GET `/retriever/info`

補足
- DocumentsAPI の `POST /documents/search` と RetrieverAPI の `POST /retriever` は **別系統**です（Base URL が異なり、レスポンス形状も異なります）。

---

#### 代表フロー
1. DocumentsAPI（4.6）でドキュメントを取り込む（埋め込み作成が完了している前提を作る）
2. RetrieverAPI（POST `/retriever`）へクエリを投げ、`results[]` の `text` と `metadata` をUI/プロンプトへ利用する

---

#### Request / Response

1) 検索: POST `/retriever`  
必須: `text`  

```json
{
  "text": "検索クエリ",
  "d_app_id": "app-123",
  "project_id": "proj-456",
  "limit": 10,
  "search_mode": "vector",
  "files_directories": ["C:\\Docs\\Guides"],
  "documents_id": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

呼び出し例

```bash
curl -X POST http://localhost:6500/iblink/v1/retriever \
  -H "Content-Type: application/json" \
  -d '{"text":"検索クエリ","d_app_id":"app-123","project_id":"proj-456","limit":10,"search_mode":"vector"}'
```

レスポンス（例）

```json
{
  "query": "検索クエリ",
  "project_id": "proj-456",
  "d_app_id": "app-123",
  "total_results": 10,
  "results": [
    {
      "id": "doc-123-chunk-5",
      "text": "ドキュメントの一部テキスト...",
      "score": 0.92,
      "metadata": {
        "file_path": "C:\\Docs\\Guides\\guide.pdf",
        "chunk_index": 5,
        "page_range": "12-14",
        "document_id": "550e8400-e29b-41d4-a716-446655440000"
      }
    }
  ]
}
```

2) ヘルス: GET `/retriever/health`  
3) 情報: GET `/retriever/info`

```bash
curl http://localhost:6500/iblink/v1/retriever/health
curl http://localhost:6500/iblink/v1/retriever/info
```

---

### 4.8 AudioAPI
概要  
AudioAPI は、IB-Link（Audio サービス）に対して **音声文字起こし（音声ファイル → テキスト）** と **ヘルス/システム情報取得** を行う HTTP API です（Whisper Server のHTTP/WSは 4.9 を参照）。

---

#### Base URL
- `http://localhost:7000/iblink/v1`

補足
- 本節（4.8）は **7000/iblink/v1 の `/audio/*`** を扱います。
- `http://localhost:7000/realtime`（SignalR / WebSocket）は `/audio/*` とは別系統です（本書では 4.15 側で扱います）。

---

#### Endpoints
- 文字起こし: POST `/audio/transcriptions`（`multipart/form-data`）
- ヘルス: GET `/audio/health`
- システム情報: GET `/audio/system/info`

---

#### 代表フロー
1. `GET /audio/health` で到達性/初期化状態を確認する
2. 必要に応じて `POST /audio/transcriptions` に音声ファイルを送信し、`text` を取得してUI/後段処理に渡す

---

#### Request / Response

1) ヘルス: GET `/audio/health`

```json
{ "status": "healthy" }
```

呼び出し例

```bash
curl http://localhost:7000/iblink/v1/audio/health
```

2) 文字起こし: POST `/audio/transcriptions`  
Content-Type: `multipart/form-data`（`FormData` を使用）
- 必須: `file`
- 例: `model=whisper-1`

レスポンス（例）

```json
{ "text": "This is the transcribed text from the audio file." }
```

呼び出し例

```bash
curl -X POST http://localhost:7000/iblink/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-1"
```

3) システム情報: GET `/audio/system/info`

```bash
curl http://localhost:7000/iblink/v1/audio/system/info
```

### 4.9 AudioNPUAPI
概要  
AudioNPUAPI は、Whisper Server（既定: `http://localhost:8000`）に対して **音声文字起こし（HTTP）** と **リアルタイム文字起こし（WebSocket）** を行うためのAPIです。

---

#### Base URL
- HTTP: `http://localhost:8000`
- WebSocket（Realtime）: `ws://127.0.0.1:8000/v1/audio/realtime`
  - `localhost` が IPv6 の `::1` を解決する環境では接続に失敗することがあるため、`127.0.0.1` を用いる例があります。

補足
- 本節（4.9）は **8000系（Whisper Server + WS realtime）** を扱います。
- 7100（`/api/whisperserver/*` の起動/停止/状態）は **別系統（4.14）**です。

---

#### Endpoints
- ヘルス: GET `/health`
- ステータス: GET `/status`
- 文字起こし（音声ファイル）: POST `/v1/audio/transcriptions`（`multipart/form-data`）
- 翻訳（音声ファイル→英語）: POST `/v1/audio/translations`（`multipart/form-data`）
- リアルタイム（WebSocket）: WS `/v1/audio/realtime`

---

#### 代表フロー
1. `GET /health` で到達性/初期化状態を確認する（`status=healthy` を待つ例があります。`whisper.status` が返る場合に `initialized` を待つ例もあります）
2. リアルタイムの場合は WS `/v1/audio/realtime` に接続し、開始設定（JSON）を送信してからPCM（16kHz/mono）を送信する
3. 受信したJSONの `text`（または `transcript` 等）をUIへ反映し、`type` / 確定フラグ（例: `is_final` / `final` / `phrase_complete`）で確定を判定する

---

#### Request / Response

1) ヘルス: GET `/health`

```bash
curl http://localhost:8000/health
```

2) ステータス: GET `/status`

```bash
curl http://localhost:8000/status
```

3) 文字起こし（音声ファイル）: POST `/v1/audio/transcriptions`

```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=json"
```

4) 翻訳（音声ファイル→英語）: POST `/v1/audio/translations`

```bash
curl -X POST http://localhost:8000/v1/audio/translations \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=json"
```

5) リアルタイム（WebSocket）: WS `/v1/audio/realtime`

開始設定（実装差分あり）
- 方式A: `{"action":"start","config":{...}}`
- 方式A（別例）: `config.vad` を含める
- 方式B: `{...}`（設定オブジェクトをそのまま送信）

方式A（送信例）

```json
{
  "action": "start",
  "config": {
    "model": "whisper-large-v3-turbo",
    "language": "auto",
    "response_format": "json",
    "sample_rate": 16000,
    "vad_enabled": true,
    "energy_threshold": 1000,
    "record_timeout": 2.0,
    "phrase_timeout": 1.0
  }
}
```

方式A（送信例: `config.vad`）

```json
{
  "action": "start",
  "config": {
    "model": "whisper-large-v3-turbo",
    "language": "auto",
    "response_format": "json",
    "sample_rate": 16000,
    "vad": {
      "enabled": true,
      "energy_threshold": 0.015,
      "silence_duration_ms": 3000,
      "min_voice_ms": 120
    }
  }
}
```

方式B（送信例）

```json
{
  "language": "auto",
  "energy_threshold": 1000,
  "record_timeout": 2.0,
  "phrase_timeout": 1.0
}
```

送信
- 開始設定の送信後、音声フレームを **バイナリ**で送信します（Int16 PCM の `ArrayBuffer` / `Uint8Array` 等）。

```javascript
// 例: Int16 PCM を送る
const int16Pcm = new Int16Array([0, 1, -1]);
ws.send(int16Pcm.buffer);
```

受信
- `payload.text` / `payload.transcript` / `payload.full_text` 等を表示テキストとして扱う実装があります
- `payload.type`（例: `partial` / `final` / `transcription`）を見て分岐する実装があります
- 確定判定は `payload.is_final === true` / `payload.final === true` / `payload.phrase_complete === true`、または `payload.type === "final"` を使う実装があります

受信例

```json
{ "type": "partial", "text": "こん", "is_final": false }
```

```json
{ "type": "final", "text": "こんにちは", "is_final": true }
```

### 4.10 EmbeddingsAPI
概要  
EmbeddingsAPI は、テキスト入力から **埋め込みベクトル（embeddings）**を生成するHTTP APIです。

補足
- 現行のDアプリ実装では、本API（`http://localhost:5000/iblink/v1`）の **直接呼び出しは確認できていません**。

---

#### Base URL
- `http://localhost:5000/iblink/v1`

---

#### 共通
- Headers
  - `Content-Type: application/json`（JSON body を送るPOSTのみ）

---

#### Endpoints
- 埋め込み生成: POST `/embeddings`
- モデル一覧: GET `/models`
- モデル情報: GET `/models/{modelId}`
- ヘルス: GET `/embeddings/health`

---

#### 代表フロー
1. `GET /embeddings/health` で到達性を確認する
2. `GET /models` で利用可能な `model` を選ぶ
3. `POST /embeddings` に `input` と `model` を送信し、`data[].embedding` を取得する

---

#### Request / Response

1) ヘルス: GET `/embeddings/health`

```bash
curl http://localhost:5000/iblink/v1/embeddings/health
```

2) モデル一覧: GET `/models`

```bash
curl http://localhost:5000/iblink/v1/models
```

3) モデル情報: GET `/models/{modelId}`

```bash
curl http://localhost:5000/iblink/v1/models/all-MiniLM-L6-v2
```

4) 埋め込み生成（単発）: POST `/embeddings`

送信フィールド（例）
- `input`: string または string[]
- `model`: string
- `encoding_format`: string（例: `float`）
- `dimensions`: number

```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The quick brown fox jumps over the lazy dog",
    "model": "all-MiniLM-L6-v2"
  }'
```

レスポンス（例）

```json
{
  "object": "list",
  "data": [
    { "object": "embedding", "embedding": [0.023064375, -0.009327292], "index": 0 }
  ],
  "model": "all-MiniLM-L6-v2",
  "usage": { "prompt_tokens": 12, "total_tokens": 12 }
}
```

5) 埋め込み生成（バッチ）: POST `/embeddings`

```bash
curl -X POST http://localhost:5000/iblink/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": ["text-1", "text-2"],
    "model": "all-MiniLM-L6-v2"
  }'
```

---

### 4.11 LlamaServerAPI

---

概要  
LlamaServerAPI は、`llama-server.exe`（llama.cpp）を **起動/停止/状態確認/モデル切り替え**するためのHTTP APIです。加えて、ローカルGGUFモデルの列挙/削除や、HuggingFaceからのモデル取得（SSE進捗）等を提供します。

---

#### Base URL
- `http://localhost:9000/iblink/v1/llama-server`

補足
- `GET /health` は `http://localhost:9000/health`（Base URL 直下）です。
- `POST /start` / `POST /switch-model` のレスポンスには `endpoint: "http://localhost:{port}/v1"` が含まれます（例: `http://localhost:8080/v1`）。この `/v1/*` は本章の対象外です（4.13 側で扱います）。

---

#### 共通
- Headers
  - `Content-Type: application/json`（JSON body を送るPOSTのみ）

---

#### Endpoints
- Server Management
  - 起動: POST `/start`
  - 停止: POST `/stop`
  - 状態: GET `/status`
  - モデル切替: POST `/switch-model`
- Model Management
  - ローカルモデル一覧: GET `/models`
  - ローカルモデル削除: DELETE `/models`（query: `modelPath`）
- Model Download（HuggingFace）
  - 検索: POST `/models/search`
  - リポジトリ情報: GET `/models/info`（query: `repository`）
  - ダウンロード: POST `/models/download`
  - ダウンロード（SSE）: POST `/models/download-stream`
- Binary Management
  - バイナリ一覧: GET `/binaries`
  - バイナリ情報: GET `/binaries/info`（query: `binaryPath`）
  - バイナリ設定: POST `/binaries/set`
- Configuration
  - 情報: GET `/info`
  - 設定更新: POST `/config`
- Monitoring
  - ログ取得: GET `/logs`（query: `lines`, `level`）
  - ログ配信（SSE）: GET `/logs/stream`
  - APIヘルス: GET `http://localhost:9000/health`

---

#### 代表フロー
1. `GET http://localhost:9000/health` で到達性を確認する
2. `GET /models` で利用可能なGGUFモデルを確認する
3. `POST /start`（または `POST /switch-model`）で推論サーバを起動し、レスポンスの `endpoint`（`http://localhost:{port}/v1`）を取得する
4. 必要に応じて `GET /status` / `GET /logs` で状態を監視し、`POST /stop` で停止する

---

#### Request / Response

1) APIヘルス: GET `http://localhost:9000/health`

```bash
curl http://localhost:9000/health
```

2) 状態: GET `/status`

```bash
curl http://localhost:9000/iblink/v1/llama-server/status
```

3) ローカルモデル一覧: GET `/models`

```bash
curl http://localhost:9000/iblink/v1/llama-server/models
```

4) 起動: POST `/start`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/start \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\model.gguf",
    "port": 8080,
    "options": {}
  }'
```

5) 停止: POST `/stop`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/stop
```

6) モデル切替: POST `/switch-model`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "C:\\Models\\Different-Model.gguf",
    "binary_path": "C:\\llama-cpp\\x64\\llama-server.exe"
  }'
```

7) モデル削除: DELETE `/models`（query: `modelPath`）

```bash
curl -X DELETE "http://localhost:9000/iblink/v1/llama-server/models?modelPath=C:\\Models\\model-to-delete.gguf"
```

8) HuggingFace検索: POST `/models/search`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/search \
  -H "Content-Type: application/json" \
  -d '{"query":"gemma gguf"}'
```

9) リポジトリ情報: GET `/models/info`

```bash
curl "http://localhost:9000/iblink/v1/llama-server/models/info?repository=ggml-org/gemma-2-2b-it-Q4_K_M-GGUF"
```

10) ダウンロード: POST `/models/download`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download \
  -H "Content-Type: application/json" \
  -d '{
    "repository":"ggml-org/gemma-2-2b-it-Q4_K_M-GGUF",
    "files":["gemma-2-2b-it-Q4_K_M.gguf"]
  }'
```

11) ダウンロード（SSE）: POST `/models/download-stream`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/models/download-stream \
  -H "Content-Type: application/json" \
  -d '{"repository":"ggml-org/gemma-2-2b-it-Q4_K_M-GGUF","files":["gemma-2-2b-it-Q4_K_M.gguf"]}' \
  -N
```

12) バイナリ一覧: GET `/binaries`

```bash
curl http://localhost:9000/iblink/v1/llama-server/binaries
```

13) バイナリ情報: GET `/binaries/info`

```bash
curl "http://localhost:9000/iblink/v1/llama-server/binaries/info?binaryPath=C:\\llama-cpp\\x64\\llama-server.exe"
```

14) バイナリ設定: POST `/binaries/set`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/binaries/set \
  -H "Content-Type: application/json" \
  -d '{"binary_path":"C:\\llama-cpp\\x64\\llama-server.exe"}'
```

15) 情報: GET `/info`

```bash
curl http://localhost:9000/iblink/v1/llama-server/info
```

16) 設定更新: POST `/config`

```bash
curl -X POST http://localhost:9000/iblink/v1/llama-server/config \
  -H "Content-Type: application/json" \
  -d '{"models_directory":"D:\\AI\\Models"}'
```

17) ログ取得: GET `/logs`

```bash
curl "http://localhost:9000/iblink/v1/llama-server/logs?lines=50"
```

18) ログ配信（SSE）: GET `/logs/stream`

```bash
curl -N http://localhost:9000/iblink/v1/llama-server/logs/stream
```

---

### 4.12 FoundryLocalAPI
概要  
FoundryLocalAPI は、FoundryLocal のローカル推論サーバを **起動/停止/状態確認/モデル切替**するためのHTTP APIです。加えて、モデルの列挙/ダウンロード/削除、ログ取得（SSE）、ヘルス確認を提供します。

---

#### Base URL
- `http://localhost:9500/iblink/v1/foundry-local`

補足
- `POST /start` / `POST /switch-model` のレスポンスには `endpoint: "http://127.0.0.1:{port}/v1"` と `api_key` が含まれます（`/v1/*`）。この `/v1/*` は本章の対象外です（4.13 側で扱います）。
- モデル一覧: `GET http://localhost:9500/v1/models`（Base URL 直下ではありません。詳細は 4.13 側で扱います）

---

#### 共通
- Headers
  - `Content-Type: application/json`（JSON body を送るPOSTのみ）

---

#### Endpoints
- Server Management
  - 起動: POST `/start`
  - 起動（SSE）: POST `/start-stream`
  - 停止: POST `/stop`
  - 状態: GET `/status`
  - モデル切替: POST `/switch-model`
- Model Management
  - モデル一覧: GET `/models`
  - ダウンロード済み一覧: GET `/models/downloaded`
  - ロード済み一覧: GET `/models/loaded`
  - 全アンロード: POST `/models/unload-all`
  - ダウンロード: POST `/models/{modelName}/download`
  - ダウンロード（SSE）: POST `/models/{modelName}/download-stream`
  - 削除: DELETE `/models/{modelName}`
- Configuration and Info
  - 情報: GET `/info`
  - 設定更新: POST `/config`
- Logging
  - ログ取得: GET `/logs`（query: `count`）
  - ログ配信（SSE）: GET `/logs/stream`
- Health
  - ヘルス: GET `/health`

---

#### 代表フロー
1. `GET /health` で到達性を確認する
2. `GET /models` で利用可能な `model_name` を確認する
3. 必要なら `POST /models/{modelName}/download` でモデルを取得する
4. `POST /start`（または `POST /switch-model`）で推論サーバを起動し、レスポンスの `endpoint`（`http://127.0.0.1:{port}/v1`）と `api_key` を取得する
5. 必要に応じて `GET /status` / `GET /logs` で状態を監視し、`POST /stop` で停止する

---

#### Request / Response

1) ヘルス: GET `/health`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/health
```

2) 状態: GET `/status`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/status
```

3) モデル一覧: GET `/models`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/models
```

4) ダウンロード済み一覧: GET `/models/downloaded`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/models/downloaded
```

5) ロード済み一覧: GET `/models/loaded`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/models/loaded
```

6) ダウンロード: POST `/models/{modelName}/download`

```bash
curl -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF/download"
```

7) ダウンロード（SSE）: POST `/models/{modelName}/download-stream`

```bash
curl -N -X POST "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF/download-stream"
```

8) 全アンロード: POST `/models/unload-all`

```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/models/unload-all
```

9) 削除: DELETE `/models/{modelName}`

```bash
curl -X DELETE "http://localhost:9500/iblink/v1/foundry-local/models/Qwen2.5-0.5B-Instruct-Q8_0-GGUF"
```

10) 起動: POST `/start`

```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/start \
  -H "Content-Type: application/json" \
  -d '{"model_name":"Qwen2.5-0.5B-Instruct-Q8_0-GGUF"}'
```

11) 起動（SSE）: POST `/start-stream`

```bash
curl -N -X POST http://localhost:9500/iblink/v1/foundry-local/start-stream \
  -H "Content-Type: application/json" \
  -d '{"model_name":"Qwen2.5-0.5B-Instruct-Q8_0-GGUF"}'
```

12) モデル切替: POST `/switch-model`

```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/switch-model \
  -H "Content-Type: application/json" \
  -d '{"model_name":"Qwen2.5-3B-Instruct-Q4_K_M-GGUF"}'
```

13) 停止: POST `/stop`

```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/stop
```

14) 情報: GET `/info`

```bash
curl http://localhost:9500/iblink/v1/foundry-local/info
```

15) 設定更新: POST `/config`

```bash
curl -X POST http://localhost:9500/iblink/v1/foundry-local/config \
  -H "Content-Type: application/json" \
  -d '{"models_directory":"D:\\AI\\Models"}'
```

16) ログ取得: GET `/logs`

```bash
curl "http://localhost:9500/iblink/v1/foundry-local/logs?count=50"
```

17) ログ配信（SSE）: GET `/logs/stream`

```bash
curl -N http://localhost:9500/iblink/v1/foundry-local/logs/stream
```

---

### 4.13 LLM推論エンドポイント（`/v1/chat/completions`）
概要  
本節は、Dアプリが利用している推論エンドポイント（`/v1/models`, `/v1/chat/completions`）を「URL/パス」で識別してまとめます。

---

#### Base URL（推論サーバ）
- `http://localhost:{port}/v1`
  - Dアプリ既定の例: `http://localhost:8080/v1`
- FoundryLocal の起動レスポンスが返す例: `http://127.0.0.1:{port}/v1`（`api_key` を伴う）

補足
- `.../iblink/v1` 配下のAPI（Documents/Retriever/各管理API）とは **別系統**です。
- 管理API（4.11/4.12）の `POST /start` レスポンスに含まれる `endpoint` が、この推論Base URLになります。
- `api_key` がある場合は、推論リクエストで `Authorization: Bearer {api_key}` を送る実装があります。

---

#### Endpoints
- モデル一覧: GET `/models`
- チャット補完: POST `/chat/completions`

---

#### 代表フロー
1. `GET /v1/models` で到達性/起動完了を確認する
2. `POST /v1/chat/completions` に `messages` を送信する
3. `stream:true` の場合は、SSE（`data: {json}\n` / `data: [DONE]\n`）を行単位で処理する

---

#### Request / Response

1) モデル一覧: GET `/models`

```bash
curl http://localhost:8080/v1/models
```

2) チャット補完（非ストリーミング）: POST `/chat/completions`

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "localmodel",
    "messages": [
      { "role": "system", "content": "あなたはアシスタントです。" },
      { "role": "user", "content": "返答をどうぞ。" }
    ],
    "temperature": 0.3,
    "max_tokens": 200
  }'
```

3) チャット補完（ストリーミング）: POST `/chat/completions`（SSE）

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "localmodel",
    "messages": [{ "role": "user", "content": "Hello!" }],
    "stream": true
  }' \
  -N
```

補足
- `503` かつ本文に `Loading model` を含む場合に、待機して再試行する実装があります。

4) チャット補完（`api_key` を送る例）: POST `/chat/completions`

```bash
curl -X POST http://127.0.0.1:1234/v1/chat/completions \
  -H "Authorization: Bearer fl-YourApiKey123" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct-Q8_0-GGUF",
    "messages": [{ "role": "user", "content": "Hello!" }]
  }'
```

---

### 4.14 音声管理エンドポイント（7100）
概要  
本節は、Whisper Server（8000）の起動/停止を制御する **音声“管理”エンドポイント**（7100系）を「URL/パス」で識別してまとめます（7000/realtime や Whisper 本体とは別系統）。

---

#### Base URL
- `http://127.0.0.1:7100`

---

#### Endpoints
- 状態: GET `/api/whisperserver/status`
- ヘルス: GET `/api/whisperserver/health`
- 情報: GET `/api/whisperserver/info`
- ログ: GET `/api/whisperserver/logs`（query: `lines`）
- 起動: POST `/api/whisperserver/start`
- 停止: POST `/api/whisperserver/stop`

---

#### 代表フロー
1. `GET /api/whisperserver/status` で起動済みか確認する
2. `POST /api/whisperserver/start` で起動する（必要に応じて `model` / `port` / `host` / `detached` を指定）
3. `GET /api/whisperserver/health` で健全性を確認する
4. `POST /api/whisperserver/stop` で停止する（誤停止を避けるため「自分が起動したものだけ止める」等の安全策を入れる実装があります）

---

#### 呼び出し例

```bash
curl http://127.0.0.1:7100/api/whisperserver/status
curl http://127.0.0.1:7100/api/whisperserver/health
curl http://127.0.0.1:7100/api/whisperserver/info
curl "http://127.0.0.1:7100/api/whisperserver/logs?lines=200"

curl -X POST http://127.0.0.1:7100/api/whisperserver/start \
  -H "Content-Type: application/json" \
  -d '{"model":"base","port":8000,"host":"127.0.0.1","detached":true}'

curl -X POST http://127.0.0.1:7100/api/whisperserver/stop \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 4.15 7000/realtime（SignalR / WebSocket）
概要  
本節は、音声のリアルタイム文字起こしで利用される `http://localhost:7000/realtime` を、**URL/パス**で識別してまとめます（通信方式は SignalR の WebSocket です）。

---

#### URL / 関連URL
- `http://localhost:7000/realtime`（SignalR / WebSocket）
- ヘルス（HTTP）: `http://localhost:7000/iblink/v1/audio/health`

---

#### 代表フロー
1. `http://localhost:7000/realtime`（`/realtime`）へWebSocket接続する
2. 受信イベント（例: `TranscriptionResult` 等）を購読し、`text` と完了フラグ（例: `phrase_complete` / `is_final` / `final`）をUIへ反映する
3. `UpdateSettings` を呼び、`SendAudio` でPCMのバイト列（`Array<number>`）を送信する（実装で観測）。必要に応じて `FlushAudio` を呼ぶ

---

#### 実装参照

```javascript
// SignalR（WebSocket）接続
const hubUrl = 'http://localhost:7000/realtime';
const conn = new signalR.HubConnectionBuilder()
  .withUrl(hubUrl, { skipNegotiation: true, transport: signalR.HttpTransportType.WebSockets })
  .withAutomaticReconnect([0, 2000, 10000, 30000])
  .build();

conn.on('TranscriptionResult', (payload) => console.log(payload));
conn.on('Connected', (payload) => console.log(payload));
await conn.start();
await conn.invoke('UpdateSettings', { chunkDurationMs: 2000, language: null, returnFinalOnly: false, enableVAD: true });
// 音声フレーム: Int16 PCM -> Uint8Array -> Array<number>
const byteArray = new Uint8Array(int16Pcm.buffer);
await conn.invoke('SendAudio', Array.from(byteArray));
// 終了時（必要に応じて）
await conn.invoke('FlushAudio');
```

到達性確認（HTTP）

```bash
curl http://localhost:7000/iblink/v1/audio/health
```

---

© 2026 IB-Link / J-AIC   
本ドキュメントの無断転載を禁じます。  

---
