## （タイトル）

### 適用範囲
- 対象アプリ: medical / retail / josys / sales
- 対象範囲: Main / Preload / Renderer / Build / API

---

## 仕様

### Request
- Body（JSON）
- Query
- Headers

### Responses
- 200
- 400
- 401/403
- 500

### ふるまい
- （事実のみ）

### 制約
- （事実のみ）

---

## 例

### Request（Body例）
```json
{
  "example": "value"
}
```

### Response（200例）
```json
{
  "success": true,
  "data": {}
}
```

---

## 差分/競合（存在する場合）
- **競合ID**: CONFLICT-YYYYMMDD-XX
- **衝突点**:
- **medical（事実）**:
- **retail（事実）**:
- **josys（事実）**:
- **sales（事実）**:
- **決定（確定している場合）**: 採用: medical / retail / josys / sales / 未決
- **競合ログ**: `90_Conflict_Log.md`

---

## 関連
- （関連するマニュアル: `xx_*.md`）
- （関連コード: `path/to/file`）

