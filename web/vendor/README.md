# Vendored dependencies

| 檔案 | 套件 | 版本 | 授權 | 來源 |
|------|------|------|------|------|
| `chart.umd.min.js` | [Chart.js](https://www.chartjs.org/) | 4.5.1 | MIT（見 `chart.js-LICENSE.md`） | npm `chart.js@4.5.1` → `dist/chart.umd.min.js`，未修改 |
| `xlsx.full.min.js` | [SheetJS Community Edition](https://sheetjs.com/)（`xlsx`） | 0.20.3 | Apache-2.0（見 `xlsx-LICENSE.txt`） | 官方 CDN `https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js`，下載後自架，執行期不載 CDN |

- SHA-256（`chart.umd.min.js`）：`48444a82d4edcb5bec0f1965faacdde18d9c17db3063d042abada2f705c9f54a`
- SHA-256（`xlsx.full.min.js`）：`cc015130aa8521e7f088f88898eba949ccdcbfb38df0bd129b44b7273c3a6f41`
- 不使用日期 adapter：時間軸一律先在 `js/types.js` 解析、排序，再以 **category 軸** 繪製，因此不需要 `chartjs-adapter-*` 與 date-fns / luxon。
- 檔尾的 `sourceMappingURL` 指向未附的 `.map`，只影響 DevTools 除錯，不影響執行。

## 更新方式

```bash
npm pack chart.js@<version>   # 或 npm i chart.js@<version> 於暫存資料夾
cp package/dist/chart.umd.min.js web/vendor/chart.umd.min.js
cp package/LICENSE.md web/vendor/chart.js-LICENSE.md
sha256sum web/vendor/chart.umd.min.js   # 更新本表

curl -fsSL -o web/vendor/xlsx.full.min.js \
  https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js
curl -fsSL -o web/vendor/xlsx-LICENSE.txt \
  https://cdn.sheetjs.com/xlsx-0.20.3/package/LICENSE
sha256sum web/vendor/xlsx.full.min.js
```

0.20.3 修了 CVE-2023-30533（prototype pollution，0.19.3）與 CVE-2024-22363（ReDoS，0.20.2）。SheetJS 只在瀏覽器本機解析 `.xlsx`／`.xls`／`.ods`，不走 CDN，也不放寬 CSP `script-src`。日期用 Excel 序號 + `XLSX.SSF.parse_date_code` 轉 ISO，不開 `cellDates`、不經主機時區。
