# API 契約草案 v0.2（mock）

- **產出**：斯考 - 後端
- **對象**：雀絲（核准）、洛彭（前端對齊）
- **日期**：2026-10-07（台北）· **v0.2**：回調網址改帶一次性授權碼；新增 `POST /v1/auth/exchange`；history 只收白名單欄位、去掉 `note`
- **範圍**：mock only；不接真實金流、不申請金流帳號
- **已定案**：MIT skill 永不付費牆；11/7 主賣 hosted Pro（個人）；登入 = GitHub OAuth；訪客示範不限、自貼每日 3 次／瀏覽器；登入後 7 天 Pro 試用

## 變更紀錄

| 版本 | 日期 | 變更 |
|------|------|------|
| v0.1 | 2026-10-07 | history→201；429 加 Retry-After／reset_at；opaque token；GET /v1/health |
| v0.2 | 2026-10-07 | 回調網址不再帶存取憑證（改帶一次性授權碼，預設約 60 秒）；新增 `POST /v1/auth/exchange`；history 嚴格白名單，去掉 `note` |

---

## 0. 共通假設

| 項目 | 假設（v0） |
|------|------------|
| Base URL | `https://api.<待老闆拍板網域>`；本地 mock `http://127.0.0.1:8787` |
| 認證 | `Authorization: Bearer <access_token>`（靜態站友善） |
| CORS | 允許 hosted 前端 origin；`Authorization`、`Content-Type` header；不依賴第三方 Cookie 作主路徑 |
| Cookie | **可選**；若日後同網域可加 `HttpOnly` session，v0 前端以 Bearer 為準 |
| Content-Type | `application/json; charset=utf-8` |
| 時間 | ISO 8601，含 `+08:00` 或 `Z` |
| 原始 CSV | **預設不存**；history 只存摘要（圖種、檔名、列數） |

### 錯誤碼

| 碼 | 意義 |
|----|------|
| `400` | 請求格式錯；授權碼無效／過期／已用（`invalid_grant`）；history 出現白名單以外欄位（`unknown_field`） |
| `401` | 未登入／token 無效 |
| `402` | 需要付費或升級（可選；額度用尽也可用 `429`） |
| `403` | 已登入但缺 entitlement／feature |
| `404` | 資源不存在 |
| `429` | 訪客每日自貼額度用尽，或 Pro／trial quota 用尽；回 `Retry-After`（秒）或 body `quota.reset_at` |
| `501` | 真實金流未接（正式 checkout 前） |

### Plan / status

| plan | status | 說明 |
|------|--------|------|
| `free` | `none` | 訪客或登入但無試用／訂閱 |
| `trial` | `trialing` | 7 天 Pro 試用中 |
| `pro` | `active` | 個人 Pro |
| `pro` | `expired` / `canceled` | 曾訂閱，已失加值 |

`features`（Pro／trial 開啟）：`save_history`、`hosted_quota`、`faster_ui`  
11/7 **不做** `team_seats`。

---

## 1. `GET /v1/me`

**用途**：頁面載入拉身分＋權限。

**Headers**：可選 `Authorization`（無則當訪客）。

**200（訪客）**

```json
{
  "user": null,
  "entitlement": {
    "plan": "free",
    "status": "none",
    "features": [],
    "quota": {
      "guest_uploads_remaining_today": 3,
      "guest_uploads_limit_per_day": 3,
      "hosted_runs_remaining": null,
      "seats": 1,
      "valid_until": null
    },
    "source": "anonymous",
    "trial_ends_at": null
  }
}
```

**200（試用中）**：`user` 含 `id`／`login`／`avatar_url`；`plan=trial`、`status=trialing`、`features` 含 `save_history`／`hosted_quota`／`faster_ui`；`trial_ends_at` = 登入起 +7 天。

訪客額度：前端可用 localStorage 對齊「每瀏覽器每日 3」；mock 可選收 `X-Guest-Id`。

---

## 2. `GET /v1/entitlement`

**200**：`{ "entitlement": { ... } }`（欄位同 `/me` 的 entitlement）。允許匿名。

---

## 3. GitHub OAuth

流程對齊真實 GitHub：前端只拿到一次性授權碼，再用伺服器端換票。回調網址**不得**帶存取憑證。

### `GET /v1/auth/github`

開始 OAuth。Mock 可回 `{ "authorize_url": "http://127.0.0.1:8787/v1/auth/github/callback?code=mock" }` 或 302。

### `GET /v1/auth/github/callback?code=...`

驗證 mock GitHub 的 `code`（缺則 `400` `missing_code`）。固定測試 user；**首次登入自動 trial 7 天**。發出**一次性、短效**授權碼（預設約 60 秒；mock 可用環境變數 `AUTH_CODE_TTL_MS` 或可注入時鐘調整）。

- `Accept: application/json` 或 `?format=json`：`200` `{ "code", "expires_in" }`（秒）。**不回** `access_token`。
- 否則 `302` 到前端，查詢字串**只帶** `code`。網址不得出現 `access_token`，也不得出現日後換到的憑證值。

不打真 GitHub（除非雀絲另准申請 OAuth app）。

### `POST /v1/auth/exchange`

**Body**：`{ "code": "..." }`  
**200**（與既有憑證回應同形）：

```json
{
  "access_token": "opaque-string",
  "token_type": "Bearer",
  "user": { "id": "1", "login": "wids-mock", "avatar_url": "..." },
  "entitlement": { }
}
```

同一支授權碼只能換一次。缺碼、未知、已用、過期一律 `400`，錯誤信封：

```json
{ "error": { "code": "invalid_grant", "message": "..." } }
```

CORS 與其他路徑相同：允許預檢、`Authorization`、`Content-Type`。

---

## 4. Checkout（mock）

### `POST /v1/checkout/session`

**Auth**：必填。  
**Body**：`{ "plan": "pro", "interval": "month" }`  
**200**：`{ "session_id", "checkout_url", "mock": true }`  
**401／400／403**（已是 active）／**501**

### `POST /v1/checkout/mock-complete`

**Body**：`{ "session_id" }` → entitlement 變 `pro`＋`active`。**404** 未知 session。

### `POST /v1/checkout/mock-cancel`

**Body**：`{ "session_id" }` → `{ "ok": true }`，權限不變。

---

## 5. History

### `GET /v1/history` / `POST /v1/history`

需 Bearer＋ feature `save_history`。  
POST body **只允許** `pattern_id`、`source_name`、`row_count`。`note` 或任何未知欄位 → `400` `unknown_field`。**不接受原始 CSV**（`400` `raw_csv_rejected`）。  
POST 成功：**201**＋`{ "id", "created_at" }`（勿用 200）。回應與清單皆不含 `note`。  
**401／403／429**（429 須含 `Retry-After` 秒或 body `quota.reset_at`）

### `GET /v1/health`

**200**：`{ "ok": true, "mock": true }`（洛彭探活；無需認證）

### Token

Mock access token：**不透明字串**即可（不必 JWT）。只經 `POST /v1/auth/exchange` 發給前端；存在 `localStorage` 的 `wids_token`，不進網址。

---

## 6. 訪客自貼計次

示範 CSV 不計次。自貼／上傳：每瀏覽器每日 **3** 次。v0 可先純前端 localStorage；可選後端 `POST /v1/guest/consume-upload`。

---

## 7. 洛彭前端對齊

1. CSP `connect-src` 加入 API origin。  
2. 登入鈕 → GitHub OAuth 流程。  
3. 頁面載入若網址有 `code`：呼叫 `POST /v1/auth/exchange`，把憑證存進 `wids_token`，立刻 `history.replaceState` 去掉 `code`（失敗也要去掉）。其餘查詢與 hash 保持原樣。不要再讀網址裡的 `access_token`。  
4. 之後照舊 `GET /v1/me`。  
5. 顯示 plan／status／試用剩餘／訪客剩餘次數。  
6. 無 `save_history` 隱藏雲端歷史；升級 CTA → mock checkout。  
7. `file://` 模式不呼叫 API。

---

## 8. Mock 實作（雀絲已准）

- 目錄：`web/api-mock/`（小 Node），分支從 `web-poc` 開，PR → `web-poc`，不 push main。  
- `MOCK_PLAN=free|trial|active`；可人工開通單一 GitHub user。  
- OAuth／checkout 全 mock；token 不透明字串。  
- 前端定案：Bearer → `localStorage` `wids_token`；API base 本機 `8787`／hosted `WIDS_API_BASE`；訪客每日 3 次純前端 localStorage。
