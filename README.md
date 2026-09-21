# what-is-the-data-saying（資料在說什麼）

Grok Build skill：當資料／報表進入 harness 時，**(1) 推薦最適視覺化類型與做法**、**(2) 協助實際產出圖表**、**(3) 維護可成長的內建範例／pattern 庫**。

面向台灣繁體中文報表讀者；程式與註解可用英文。

## 安裝（Grok Build）

擇一即可：

```bash
# 推薦：以 plugin 安裝（skills 會出現在 slash menu）
grok plugin install g0uv4/what-is-the-data-saying --trust

# 或：clone 成 user skill
git clone https://github.com/g0uv4/what-is-the-data-saying.git ~/.grok/skills/what-is-the-data-saying-src
# 若採此法，請把 skills/what-is-the-data-saying 指到（或複製到）
#   ~/.grok/skills/what-is-the-data-saying/
mkdir -p ~/.grok/skills
cp -R skills/what-is-the-data-saying ~/.grok/skills/what-is-the-data-saying
```

確認：

```bash
grok plugin details what-is-the-data-saying
# 或
grok inspect | rg -i 'what-is-the-data-saying|資料'
```

使用：在 Grok TUI 輸入 `/what-is-the-data-saying`，或直接貼上資料／報表並說「這份資料該怎麼畫」。

## 每日改進怎麼做

1. **用真實報表跑一次** → 記下推薦是否命中、產出是否可用。
2. **命中新 pattern** → 在 `skills/what-is-the-data-saying/examples/` 新增一個命名 pattern（短、可複用、含 data shape + 推薦圖型 + 產出要點）。
3. **啟發式錯了** → 只改 `references/` 裡對應的單一來源檔（不要在 SKILL.md 重複貼一大段）。
4. **commit / push `main`** → 其他人 `grok plugin update what-is-the-data-saying` 即可跟上。

原則：一個事實一個家（one home per fact）；SKILL.md 管流程，細節放 references／examples。

## 版權與範圍

Private repo 預設即可；若要分享 skill，把 visibility 改 public 即可。不做 Origin；只走 GitHub。
