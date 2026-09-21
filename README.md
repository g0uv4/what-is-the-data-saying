# what-is-the-data-saying（資料在說什麼）

Grok Build skill：**v0.2.0**（納茲教圖實戰版）。當資料／報表進入 harness 時，**(1) 推薦最適視覺化類型與做法**、**(2) 協助實際產出圖表**、**(3) 維護可成長的內建範例／pattern 庫**。

面向台灣繁體中文報表讀者；程式與註解可用英文。圖種中文名、適不適合、口述怎麼做對齊納茲（資料視覺）teach-viz 教圖——見 `skills/what-is-the-data-saying/ATTRIBUTION.md`。

## 安裝（Grok Build）

擇一即可：

```bash
# 推薦：以 plugin 安裝（skills 會出現在 slash menu）
grok plugin install g0uv4/what-is-the-data-saying --trust

# 或：本地 path
grok plugin install /path/to/what-is-the-data-saying --trust
```

確認：

```bash
grok plugin validate .
grok plugin details what-is-the-data-saying
```

使用：在 Grok TUI 輸入 `/what-is-the-data-saying`，或直接貼上資料／報表並說「這份資料該怎麼畫」。

## 內容結構

- `skills/what-is-the-data-saying/SKILL.md` — 流程
- `references/chart-heuristics.md` — 任務→圖種（含易混口訣）
- `references/how-to-produce.md` — 納茲風格口述產出
- `references/data-shape-checks.md` / `taiwan-report-readers.md`
- `examples/` — 39 個具名 pattern（含來源檔名）
- `ATTRIBUTION.md` — 納茲教圖對照表

## 每日改進

1. 用真實報表跑一次 → 記推薦是否命中。
2. 新 pattern → `examples/<slug>.md` + README 列 + ATTRIBUTION。
3. 啟發式錯了 → 只改 `references/` 單一檔。
4. commit／push `main` → `grok plugin update what-is-the-data-saying`。

## 版權與範圍

Private repo 預設即可。不做 Origin；只走 GitHub。
