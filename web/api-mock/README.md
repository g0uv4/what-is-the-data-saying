# web/api-mock — 訂閱／權限 mock API

本機 Node HTTP 伺服器，實作契約 v0／v0.1 的路徑與錯誤碼。不接真實 GitHub OAuth、不接金流、不申請 OAuth app、不走 Workers。

預設聽 `http://127.0.0.1:8787`。Token 是不透明字串（不是 JWT）。

## 目錄骨架

```
web/api-mock/
├── package.json          npm start / npm test
├── server.mjs            入口；預設 port 8787
├── README.md
├── lib/
│   ├── app.mjs           路由與契約行為
│   ├── store.mjs         記憶體：user／token／checkout／history／訪客額度
│   ├── http.mjs          CORS、JSON、錯誤碼
│   └── time.mjs          台北 +08:00
└── test/
    └── smoke.test.mjs    打通主路徑的煙霧測試
```

## 怎麼跑

Node ≥ 18，無 npm 依賴。

```bash
cd web/api-mock
npm start
```

另一個終端：

```bash
curl -sS http://127.0.0.1:8787/v1/health
# {"ok":true,"mock":true}

curl -sS http://127.0.0.1:8787/v1/me
# 訪客：user=null、plan=free、guest_uploads_limit_per_day=3
```

煙霧測試（自己起臨時 port，不必先 `npm start`）：

```bash
cd web/api-mock
npm test
```

## 環境變數

| 變數 | 預設 | 說明 |
|------|------|------|
| `PORT` | `8787` | 聽哪個 port |
| `HOST` | `127.0.0.1` | bind 位址 |
| `CORS_ORIGIN` | `*` | 允許的前端 origin；也允許 `Authorization`、`X-Guest-Id` |
| `FRONTEND_ORIGIN` | `CORS_ORIGIN`（若不是 `*`）或 `http://127.0.0.1:4173` | OAuth callback 302 要帶 token 回去的前端 |
| `PUBLIC_BASE_URL` | 依 request Host | `authorize_url`／`checkout_url` 的前綴 |
| `MOCK_PLAN` | 未設 | 見下節 |
| `MOCK_FORCE_ACTIVE_GITHUB_IDS` | 空 | 逗號分隔 GitHub user id；這些人一律視為 `pro`＋`active`（人工開通） |
| `MOCK_HOSTED_RUNS` | `100` | trial／pro 的 `hosted_runs_remaining` 種子 |

狀態存在記憶體：重啟伺服器就清空。登入後的試用／checkout 會覆寫該使用者的記憶體狀態，不必重設 `MOCK_PLAN`。

### `MOCK_PLAN`

決定**固定測試帳**（`id=1`／`login=wids-mock`）第一次登入時的預設權限，方便示範：

| 值 | 第一次 callback 的 entitlement |
|----|--------------------------------|
| 未設 | 自動給 7 天 Pro 試用（`trial`／`trialing`） |
| `trial` | 同上，`source=mock_plan` |
| `free` | 已登入但無試用／訂閱（方便示範升級 CTA） |
| `active` | 直接 `pro`／`active` |

之後仍以記憶體為準：mock checkout 完成會變成 `pro`／`active`；試用到期變回 `free`／`none`。`MOCK_FORCE_ACTIVE_GITHUB_IDS`（或 store 內的 in-memory set）可強制單一 GitHub id 為 `active`，蓋過上述狀態。

```bash
MOCK_PLAN=free npm start
MOCK_PLAN=trial npm start
MOCK_PLAN=active npm start
MOCK_FORCE_ACTIVE_GITHUB_IDS=1 npm start
```

## 行為摘要

- `GET /v1/health` → `{ "ok": true, "mock": true }`
- `GET /v1/me`：Bearer 可選；沒有就是訪客
- `GET /v1/entitlement`：欄位同 `/me` 的 entitlement；允許匿名
- `GET /v1/auth/github`：預設 JSON `{ authorize_url }`；`?redirect=1` 則 302
- `GET /v1/auth/github/callback?code=...`：固定測試 user；缺 code → 400。`Accept: application/json` 或 `?format=json` 回 token；否則 302 到前端並帶 `access_token`
- `POST /v1/checkout/session`：需登入；body `{ "plan": "pro", "interval": "month" }`。已是 `active` → 403；`provider` 不是 mock → 501
- `POST /v1/checkout/mock-complete`／`mock-cancel`：用 `session_id`；未知 → 404
- `GET`／`POST /v1/history`：需 Bearer 且有 `save_history`。POST 成功 **201**＋`{ id, created_at }`。只收摘要（`pattern_id`、`source_name`、`row_count`、可選 `note`），拒絕原始 CSV
- 所有 **429** 帶 `Retry-After`（秒）以及 body `quota.reset_at`
- 訪客自貼每日 3 次（`X-Guest-Id` 可選）。**示範 CSV 不計次**（`POST /v1/guest/consume-upload` 傳 `kind=demo` 或 `source=demo`）
- trial／pro 功能：`save_history`、`hosted_quota`、`faster_ui`。沒有 team seats（`seats` 恆為 1）
- MIT skill 沒有付費牆；這支 API 只服務 hosted 網頁 PoC

## 本機打通登入與歷史

```bash
TOKEN=$(curl -sS 'http://127.0.0.1:8787/v1/auth/github/callback?code=mock&format=json' \
  | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>console.log(JSON.parse(s).access_token))")

curl -sS -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8787/v1/me

curl -sS -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"pattern_id":"lollipop-rank","source_name":"demo.csv","row_count":12}' \
  http://127.0.0.1:8787/v1/history
```
