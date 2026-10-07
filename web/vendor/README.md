# Vendored dependencies

| 檔案 | 套件 | 版本 | 授權 | 來源 |
|------|------|------|------|------|
| `chart.umd.min.js` | [Chart.js](https://www.chartjs.org/) | 4.5.1 | MIT（見 `chart.js-LICENSE.md`） | npm `chart.js@4.5.1` → `dist/chart.umd.min.js`，未修改 |
| `xlsx.full.min.js` | [SheetJS Community Edition](https://sheetjs.com/)（`xlsx`） | 0.18.5 | Apache-2.0（見 `xlsx-LICENSE.txt`） | npm `xlsx@0.18.5` → `dist/xlsx.full.min.js`，未修改 |

- SHA-256（`chart.umd.min.js`）：`48444a82d4edcb5bec0f1965faacdde18d9c17db3063d042abada2f705c9f54a`
- SHA-256（`xlsx.full.min.js`）：`c9506197caf809a075b6dee1da0d36fb19da7158ffe8a88e7b0c96c5d8623c99`
- 不使用日期 adapter：時間軸一律先在 `js/types.js` 解析、排序，再以 **category 軸** 繪製，因此不需要 `chartjs-adapter-*` 與 date-fns / luxon。
- 檔尾的 `sourceMappingURL` 指向未附的 `.map`，只影響 DevTools 除錯，不影響執行。

## 更新方式

```bash
npm pack chart.js@<version>   # 或 npm i chart.js@<version> 於暫存資料夾
cp package/dist/chart.umd.min.js web/vendor/chart.umd.min.js
cp package/LICENSE.md web/vendor/chart.js-LICENSE.md
sha256sum web/vendor/chart.umd.min.js   # 更新本表

npm pack xlsx@0.18.5
cp package/dist/xlsx.full.min.js web/vendor/xlsx.full.min.js
cp package/LICENSE web/vendor/xlsx-LICENSE.txt
sha256sum web/vendor/xlsx.full.min.js
```

SheetJS 只在瀏覽器本機解析 `.xlsx`／`.xls`／`.ods`，不走 CDN，也不放寬 CSP `script-src`。
