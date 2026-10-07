# Pattern: marey-chart

> **圖種**：馬雷圖／列車運行圖（Marey chart；train graph；time–distance diagram；stringline）
> **來源（專案維護者整理）**：`teach-viz/2026-10-05-am-marey.md`（方法教學；正式課程；首次以馬雷圖為主題）
> **亦稱**：列車運行圖（train graph，列車圖）；英文別名 Marey diagram、time–distance diagram（時間－距離圖）、time–space diagram（時空圖）、stringline／string line chart（美國交通業者的貼文與開源工具常用）、graphical timetable（圖形時刻表）；德文 Bildfahrplan（亦稱 grafischer Fahrplan、Trassengrafik、Zeit-Weg-Diagramm）；日文ダイヤグラム（簡稱ダイヤ，也叫運行図表、列車運行図表；日本說「ダイヤ改正」就是改這張圖）。「拉線圖」是課程稿自己的譯法，沒有通用中文名。英文維基百科以「Time–distance diagram」為條目名，該條目沒有提到 Marey、Ibry 或 Petiet。
> **核心**：橫軸放一天中的時刻，縱軸依**實際距離**排出沿線各站，每一班車畫成一條線；線越陡車越快，水平段是停站，兩條線交叉就是兩班車在那個時間、那個地點相遇。
> **一句話**：這條路線上每一班車在每個時間到了哪裡？——它**不是**單一指標隨時間的走勢（折線圖），也**不是**專案每項工作的起訖（甘特圖）。
> **誠實提醒**：本課是方法教學；模擬圖與本 repo 的練習資料都是虛構，**數字未核**（專案維護者整理時未核），不代替任何鐵路公司的正式時刻表或事故調查。素材包**沒有實測任何軟體**。
> **潤稿狀態**：素材包與課程終稿都明說**沒有經過 Gemini 潤稿**（Gemini 登入失效），也沒有改用其他模型潤稿；課程終稿只由手工調整措辭（把縮寫與工作用語改成白話），文字是審後由人工整理的原稿。
> **撞名**：中文維基百科輸入「运行图」會被重新導向到「趨勢圖」（run chart，品質管理用的時間序列折線圖），與列車運行圖是不同東西；中國新聞常見的「實行新的列車運行圖」指的是**營運計畫本身**（哪些車、幾點開），不是圖表畫法。馬雷圖的「斜率」是速度，與「坡度圖」（`slope-two-period.md`，兩期升降比較）也不是同一件事。

## 十六件必須釘清的事

1. **怎麼讀。** 斜率＝速度（線越接近垂直，車越快）；水平段＝停站；同方向兩線之間的間距＝班距；對向兩線交叉＝兩車在那個時間、那個地點相遇；同向兩線交叉＝超車（或追上）；計畫線與實際線在同一站的水平距離＝該站誤點分鐘。縱軸必須依實際距離排站，否則斜率不再代表速度（第 9 點）。
2. **為什麼叫「馬雷」（原始揭露＋推論）。** 法國生理學家 Étienne-Jules Marey《La Méthode Graphique》**1878 年首版**（**1885 年是另有 Masson 出版社的版本，是版次年份**）收錄一張 Paris 到 Lyon 的列車圖，書中圖名寫「依 Ibry 的方法」，內文寫發明這種圖表式運行表的功勞要歸於 Ibry 先生（法文維基文庫轉錄 1885 年版第二章；**我另外抓下該頁文字，確認有「On doit à M. Ibry l'invention de tableaux graphiques」與圖名「d'après la méthode de Ibry」**）。Edward Tufte《The Visual Display of Quantitative Information》（課程稿寫 1983 年首版、2001 年第二版）第 31 頁引用這張圖，所以資料視覺圈常稱馬雷圖；但「**因為 Tufte 引用才習慣叫馬雷圖」只是推論，無法證實**。Rendgen 指出這種圖「常被誤歸給 Marey」。
3. **Tufte 第 31 頁的圖說歸給 Ibry（原始揭露，書頁圖說）。** 正文寫「Marey's graphical train schedule for Paris to Lyon in the 1880s」，圖說寫「E. J. Marey, La méthode graphique (Paris, 1885), p. 20. The method is attributed to the French engineer, Ibry.」。課程稿讀的是美國專利審理委員會公開證物中的書頁與第二版掃描檔，**沒有看實體書**；**我另外下載該證物 PDF，文字層確實有「1885), 20. The method is attributed to the French engineer, Ibry.」與「Marey's graphical train schedule for Paris to Lyon in the 188os」**（OCR 把 0 認成 o）。Chartography 寫「Tufte 書內只歸功 Marey」與書頁圖說不符，本檔不採用。
4. **Tufte 書封面（原始揭露，第二版版權頁）。** 版權頁寫「封面圖由 Minoru Niijima 繪製，依 E. J. Marey 在 La méthode graphique（Paris, 1885）中的 Paris 到 Lyon 列車表」。所以封面是**依 Marey 書中那張圖重繪的雙色版，不是書頁掃描，也沒有站名與時刻**。課程稿讀的是**第三方書本掃描檔，沒有看實體書**（我也沒有看到版權頁，只轉載）。Rendgen 與 Chartography 兩邊其實都說封面用的是 Marey 書中的列車圖，沒有互相矛盾；Rendgen 文章裡另外展示的 1852 年 Paris 到 Boulogne 圖是別的例子，**不是封面**。
5. **Ibry 是誰（僅轉載，二手來源）。** 名字是 Charles Ibry（有文件拼成 Ybry），1847 年任巴黎－魯昂鐵路的營運副主管；依據是法國公共工程期刊《Annales des ponts et chaussées》1847 年 Baude 報告，**只有二手來源**（里昂第一大學文件與 Rendgen、Chartography 轉述；Baude 報告全文沒有讀到）。「1885」是 Marey 書的版次年份，不是 Ibry 的年份。課程稿另轉述同一份文件引述的報告註記：Busche 工程師自 1848 年 5 月 1 日起在北方鐵路用類似圖表（僅轉載；素材包本文沒有這句）。
6. **Petiet（僅轉載，單一來源）。** 德文維基百科寫已知最早在 1840 年代由法國北方鐵路公司使用，Léon Lalanne 把發明歸給工程師 Jules Petiet。Chartography 整理為：1842 年凡爾賽返程列車事故後，Petiet 在 1843 年 6 月 5 日的《Journal des chemins de fer》發表事故技術分析，同一期另發表一種新圖（列車行駛與編組的幾何描繪），該圖已佚失、只剩文字描述；**這個說法只有 Chartography 一個來源**。里昂第一大學文件用條件語氣寫那次事故「可能促成」採用這種圖，**不能寫成因果**；凡爾賽事故一律用條件語氣。
7. **俄國 Sergeev 中尉（單一來源，僅轉載）。** Friendly 與 Denis 的資料視覺化里程碑頁（datavis.ca）1885 年條目寫「新證據顯示 Sergeev 中尉約 30 年前就在俄國發展這個方法」，1854 年條目記載聖彼得堡到莫斯科 35 站的圖形時刻表；背後依據是 Wainer、Harik、Neter 2013 年《Chance》雜誌文章（題目是疑問句；付費，全文沒有讀到）。**1854 年晚於 Petiet（1843）和 Ibry（1847）**，「約 30 年前」是相對 1885 年版說的，**不能寫成「俄國較早」**。引用請引 datavis.ca 頁面，不要引 Friendly 里程碑第 6 節（該頁沒有這句話）。X 第 2 則貼文提到「俄國」，只是轉述，不是獨立來源。
8. **歷史歸屬一律用限定語，不要寫成定論。** 無法證實的有：「巴黎－里昂－地中海鐵路」這個公司名稱與該圖時刻的實際年份（來源只寫 Paris 到 Lyon，Tufte 寫「1880 年代」）、Tufte 引用的因果、「北美交通規劃人員常用拉線圖」、Petiet 1843 年新圖的內容。Baude 1847 年報告與 Wainer 等人 2013 年文章全文都沒有讀到。可以放心寫的只有：Marey 書收錄這張圖並把方法歸給 Ibry（原始揭露）；Tufte 第 31 頁圖說同樣歸給 Ibry；Tufte 封面是依 Marey 書中那張圖重繪（版權頁）；「1885」是版次年份。
9. **站距要依實際距離排，不要等距（S6）。** 同一班車每段都是時速 60 公里（各段 2、2、14、2、10 公里＝行駛 2、2、14、2、10 分鐘；站點在 0、2、4、18、20、30 公里）。六站等距排列時，每段在圖上都只佔 1 格，視覺斜率＝1 格 ÷ 行駛分鐘：丙到丁是 1／14 格每分鐘，是五段中最平的，其他 2 公里段是 1／2（7 倍），戊到己是 1／10；讀者會誤以為丙到丁最慢。依實際距離排列時五段斜率都是 1 公里每分鐘。若刻意等距，圖上要寫「斜率不代表速度」。
10. **讀點句要有精確時刻與位置；圖面寫「約」時，精確值要附上（S1、S2、S3、S8）。** S1：101 次 06:00 從甲站開、102 次 06:10 從己站開，每分鐘 1 公里、每站停 1 分鐘（丁站 06:22–06:23）；兩線在 **06:24:30、距甲站 21.5 公里**交叉，在丁站與戊站之間。S8：501 次 10:00 從甲站開、10:22 到丁站；502 次 10:05 從丁站開、10:27 到甲站；兩線在 **10:13:30、11.5 公里**交叉，在丙站與丁站之間。S3 見下一點。S2：普通 201 次 07:00 開、時速 60 公里，在丁站待避 3 分鐘（07:22–07:25）；快車 301 次 07:14 從甲站開、時速 120 公里（35 公里 17.5 分鐘）不停站、07:31:30 到己站；快車線與普通車線只交叉一次：**07:24:00，丁站（20 公里）**，正好在待避時段內；若普通車不待避（只停 1 分鐘），快車會在 **07:25:00、22 公里**（丁站與戊站之間，不是車站）追上它；快車比有待避的普通車早 9.5 分鐘到己站（07:31:30 對 07:41）。**S1、S3、S8 圖說的「約」值與資料的精確值相同**（我用分數重算：06:24:30／21.5、08:23:30／20.5、10:13:30／11.5 都是精確值，不是四捨五入）。
11. **單線區間：交叉點落在站內才是交會，落在站間就是衝突（S3）。** 下行 401 次 08:00 從甲站開、08:27 到戊站、08:28 開；上行 402 次 08:08 從己站開、08:19 到戊站後等 9 分鐘到 08:28。兩車實際線只有一處重合：**08:27–08:28 同時停在戊站**（有會車設備）。若上行車不等就開（08:20 離開戊站），兩線在 **08:23:30、20.5 公里**交叉，在丁站與戊站之間的單線區間＝正面衝突。乙、丙、丁、戊四站標為可交會（◎）。我用分數重算：401 與 402 的實際線只在戊站（24 公里）08:27 與 08:28 相接，與 402 不等就開的線只交叉一次（08:23:30、20.5 公里）。
12. **計畫對實際：寫「到站晚幾分鐘」，並說明從哪一站開始擴大、原因是停站還是行駛（S4）。** 計畫 07:00 開、07:39 到己站；實際 07:46 到己站。到站晚分鐘：乙 1、丙 2、丁 7、戊 7、己 7（離站晚：乙 2、丙 4、丁 7、戊 7）。丙站停 3 分鐘（計畫 1 分），丙到丁實際開 14 分鐘（計畫 11 分）。7 分鐘誤點的組成：甲到乙行駛 +1、乙站停站 +1、丙站停站 +2、丙到丁行駛 +3，其餘各段各站 +0；其中丙站與丙到丁共 +5，即 7 分鐘中的 5 分鐘（5／7＝71.4%，四捨五入到小數第一位），之後維持晚 7 分。
13. **公車串車與模型假設（S5）：圖說的「間隔」有兩種定義，不能混用。** 5 輛車、13 個站牌（第 0–12 站，每站相隔 1 公里），表定班距 8 分鐘；3 號車晚 3 分鐘出發（第 0 站 17:19 到），4 號車準時（17:24），起點只差 5 分鐘。**圖面與圖說的「相隔」＝兩車到站時刻的差（headway）**：3、4 號車逐站 5、4.5、3.95、3.37、2.77、2.15、1.5、0.81、0.2（之後第 8–12 站都是 0.2）分鐘，**第 7 站首次不到 1 分鐘（0.81）**；2→3 號車從 11 拉大到 16.13（圖說寫 16.1）；4→5 號車起點 8、終點 9.76（圖說寫 9.8）。**精確度提醒：** 4→5 號車的間隔並不是一路拉大——第 8 站最大（**11.18**），之後回縮到 9.76；圖說的「8 拉大到 9.8」只是起點對終點的比較。**模型裡的 g 是另一個量：g＝本車到站時刻減前車在同一站的離站時刻**（1 號車沒有前車，g 用表定班距 8 分鐘）；停站時間＝max(0.3 分鐘，0.08×g)，站間行駛 2 分鐘，不准超車（跟車至少比前車晚 0.2 分鐘離站）。所以圖說的「停站時間＝0.08 × 與前車間隔」在程式裡指的是 g，**和圖上讀到的「相隔」不同**（我重算：3→4 號車第 0 站相隔 5.0、g 4.17；4→5 號車第 0 站相隔 8.0、g 7.67，終點相隔 9.76、g 8.51；3→4 號車第 7 站起 g 為負，停站就取最小值 0.3 分鐘，再受 0.2 分鐘跟車限制）。**0.2 分鐘是模型規定的最小跟車間隔（第 8–12 站 4 號車離站都剛好比 3 號車晚 0.2 分鐘），不是觀察值。** 5 號車 18:04:48 到第 12 站。
14. **班次太密就拆圖（S7）。** 全天雙向 **284 班**全部疊在一起只剩線網；右圖只放大 07:00–09:00（不含 09:00 整）從甲站出發的下行車，共 **16 班**。精確數字：普通車 218 班（每 10 分鐘一班雙向各一，下行 05:00–23:00 含兩端共 109 班，上行晚 5 分鐘也是 109 班）＋快車 66 班（每 30 分鐘一班雙向各一，下行 06:03–22:03、上行 06:08–22:08，各 33 班）＝284 班；放大圖＝普通 12（07:00、07:10…08:50）＋快車 4（07:03、07:33、08:03、08:33）＝16 班，占全天 16／284＝**5.6%**（四捨五入到小數第一位）。同一分鐘最多有 10 班車同時在線（普通車全程 39 分鐘、快車 17.5 分鐘）。我用 pandas 重算全部計數，與素材包一致。
15. **圖說說得比圖多，或把圖的脈絡說錯。** 素材包已發現並更正的例子：R18 圖面 00:00–00:30 數得到 7 條藍線，Commons 說明與原稿寫 6 班，以圖面為準並註明不一致；R12 的區域列車（TER）與高速列車（TGV）同為紅色，不是每種車各一種顏色；R20 圖例中 ET1021 只有實際線、沒有表定線；R14 兩車交叉點落在桃山站那條線上（站內交會），不是站間途中；R13 圖面沒有可讀站名與時刻，「真實」只依 Commons 說明，僅轉載；R8 的「區域快鐵」在頁面上找不到；R21 一張照片只能證明這個調度室牆上有一份印本，不能推論全國都還在用。**軸向要標明**：時間在橫軸（R1、R14–R17，Marey 原圖與日本常見）或縱軸（R7、R11，德國與瑞典例）兩種都有，全篇固定一種。**R10 把分岔的路網壓成一條線**（Bangalore 市區外開列車，只含週一到週六行駛的列車），要在說明裡寫明。**R20 事故還原的語氣：** 2016 年 7 月 12 日 Andria 與 Corato 之間單線區間正面相撞（英文維基百科：23 死、54 傷）；義大利基礎建設與交通部 2017 年的調查報告認為直接原因是把 ET1642 與 ET1016 混淆；圖只能顯示相撞位置與時間（約 11:05，英文維基百科列 11:06，調查報告表為 11:05:20），原因判斷要引調查報告。
16. **圖片授權與來源要逐張標。** 20 張真實／示意圖（Commons）各有個別作者與授權（見最下方圖檔段）；**圖號是 R1、R3–R21，沒有 R2**——原 R2 是 1879 年《Popular Science Monthly》第 15 卷的英文標示重繪轉載版（公有領域），圖面是英文的 NOON、MIDN'T，不是同一張掃描，課程稿不嵌圖，**編號不重排**，Commons 頁面連結只留在 R1 說明。**R14（JR 西日本奈良線運行圖局部）授權有效性無法證實，建議不要放進任何對外 skill**：頁面授權欄標 GFDL＋CC BY 3.0、說明欄標 GFDL＋CC BY-SA 3.0，兩邊不一致；來源欄寫這是 JR 西日本奈良線的列車運行圖表，等於複製公司運行圖表的衍生作品，原著作權屬 JR 西日本，上傳者自行授權是否有效無法證實。**本檔不連結 R14，也不把它當可用素材。** 歷史掃描與翻拍（R3–R6）屬轉載或衍生作品；R10 使用時須保留圖面署名「Arun Ganesh, National Institute of Design Bangalore」與資料來源 indiarailinfo.com 並附頁面連結。

## When

- 有一條可以排成**一維順序**的路線（車站、站牌、里程樁），每個移動物體（列車、公車）在每個位置有時刻（到站、離站或定位紀錄）：排班找衝突（同向追撞、單線會車、超車）、比計畫與實際（誤點從哪裡開始）、看公車串車；英文維基百科還提到時間－距離圖也用在管線、鐵路、橋梁、隧道、道路等線性工程的施工排程
- 資料欄位最少要有：車次、站名（或站牌）、站點距離（公里）、到站時刻、離站時刻
- 情境（課程稿）：某條通勤鐵路（或一條公車路線）檢討平日早上的營運——快車跟普通車有沒有互相卡住？哪一站的待避讓普通車等太久？誤點從哪裡開始？公車有沒有串車？
- **不適合**：沒有一維路線順序（整個公車路網、計程車在城市裡亂跑——縱軸排不出合理順序，改用地圖或流量地圖）；班次太多又不拆圖（一天幾百班疊在一起只剩一片色塊）；站距不依實際距離又沒有說明

## Recommend

- **主選**：馬雷圖，一班車一條線；用顏色或線型分類（方向、車種、計畫對實際：虛線對實線）
- **口述步驟**（課程稿第 6 節）：
  1. 確認有一條一維路線：列出沿線站點（或站牌、里程樁）的順序與實際里程；路網就挑一條路線、一個方向軸來畫
  2. 整理時刻資料：每班車一列，記下在每站的到站與離站時刻（起點只有離站，終點只有到站）；計畫時刻表或車輛定位換算出的實際時刻都可以。台灣鐵路可用政府資料開放平臺的鐵路時刻表（國營臺灣鐵路股份有限公司提供、每日更新，採政府資料開放授權條款第 1 版）；公車可用大眾運輸開放資料格式（GTFS）或即時定位資料
  3. 決定軸向：時間橫軸、站點縱軸，或反過來；全篇固定一種，軸標寫清楚
  4. 站點依實際距離排列，不要等距，斜率才等於速度
  5. 每班車畫一條線：依序連起「到站→離站→下一站到站」；同站到站與離站之間是水平段（停站）
  6. 用顏色或線型分類（方向、車種、計畫對實際）；圖例放在不擋線的位置
  7. 標出關鍵事件：超車點、交會點、誤點擴大段、串車開始的站；單線路線要標出哪些站能會車
  8. 太密就拆：依尖峰、方向或車種拆成多張，或做一張全天總覽加一張放大圖
- **解讀**：線越陡＝車越快、線變平＝那段開得慢（可能壅塞或限速）；水平段越長＝停站越久，普通車在某站出現長水平段、旁邊有快車線穿過＝待避；同方向兩線越靠越近、最後重疊＝追上或串車；對向兩線交叉＝相遇，單線路線上交叉點必須落在能會車的車站
- **圖說建議**（素材包第 6 節）：寫清楚資料與單位（「虛構路線：甲 0、乙 6、丙 9、丁 20、戊 24、己 35 公里」；真實資料要寫日期、方向、資料來源、時間在哪個軸）；讀點句要有精確時刻與位置（「兩線在 06:24:30、距甲站 21.5 公里交叉，在丁站與戊站之間」；圖面寫「約」時，圖說或附註寫精確值）；交會要說在站內還是站間；計畫對實際要寫「到站晚幾分鐘」並說明從哪一站開始擴大；模擬圖標模擬、結尾寫「數字虛構」
- **參數與判準範例（範例，不是標準）**：

| 項目 | 數值與出處 | 性質 |
|---|---|---|
| 站距 | 依實際距離排列；等距時圖上寫「斜率不代表速度」（S6） | 範例，不是標準 |
| 單線交會 | 交叉點落在有會車設備的站內才是交會，落在站間＝衝突（S3） | 範例，不是標準 |
| 誤點歸因 | 7 分鐘中丙站停站 +2 與丙到丁行駛 +3 共 5 分鐘＝71.4%（S4） | 範例，不是標準 |
| 串車判讀 | 兩車相隔（到站時刻差）首次不到 1 分鐘的站（S5：第 7 站 0.81）；模型最小跟車間隔 0.2 分鐘是規定值 | 範例，不是標準 |
| 班次密度 | 全天雙向 284 班只剩線網；放大 07:00–09:00 下行 16 班（5.6%）（S7） | 範例，不是標準 |
| 模擬圖的班數 | 2 到 5 班車（S7 是 284 班），僅為示意 | 範例，不是標準 |

## 與鄰近圖種的區別

本表是素材包的概述，除標明出處者外沒有逐項查證來源。

| 圖種 | 它回答什麼 | 和馬雷圖的區別 |
|---|---|---|
| 折線圖（[`time-series-trend.md`](time-series-trend.md)） | 一個指標隨時間的變化 | 折線圖通常一條線是一個指標；馬雷圖一條線是**一個移動物體的位置**隨時間變化，同一張圖可有上百條線，而且**交叉本身就有意義**（相遇或超越），縱軸是實際位置而不是指標大小 |
| 甘特圖（[`gantt-schedule.md`](gantt-schedule.md)） | 每件工作的起訖時間 | 甘特圖每條橫棒是一件工作，縱軸是工作清單，**沒有空間軸**；馬雷圖的縱軸是實際位置，線是斜的，斜率就是速度 |
| 一般表列式時刻表 | 單一車站或單一班次的時刻 | 查單站或單班最快，但看不出超車、會車、誤點如何累積；馬雷圖是同一份時刻資料畫成圖。畫馬雷圖的第一步就是把表列式時刻表整理好（S8 步驟 1） |
| 趨勢圖（run chart；中文維基「运行图」的轉址頁） | 單一品質指標的走勢 | 與列車無關，只是中文名稱容易混；看流程是否受控見 [`control-chart.md`](control-chart.md) |
| 小多圖（[`small-multiples.md`](small-multiples.md)） | 同尺度並排多張小圖 | 班次太密時，可依尖峰、方向或車種拆成小多圖；本檔的拆圖是一種用法 |
| 坡度圖（[`slope-two-period.md`](slope-two-period.md)） | 兩期之間每個實體的升降 | 只有兩個時點、線的斜率是升降；馬雷圖的斜率是速度，時間軸連續 |

判斷口訣：**要看每一班車在每個時間到了哪裡、哪裡會車超車 → 馬雷圖；單一指標隨時間 → 折線圖；工作起訖 → 甘特圖；縱軸排不出一維順序 → 地圖或流量地圖。**

## Avoid

- 站點等距排列卻把斜率當速度讀（S6）；刻意等距卻不寫「斜率不代表速度」
- 把整個路網（或計程車軌跡）硬壓成一條線卻沒說明（R10）
- 一天幾百班疊在一起不拆圖、不放大（S7）
- 單線區間的交叉點落在站間，卻當成「交會」（S3）；沒說交會是在站內還是站間
- 圖說的數字和圖面的「約」值不附精確值；把 S5 的 headway 和模型的 g 混為一談；把「8 拉大到 9.8」說成一路拉大
- 把歷史寫成定論：把 Tufte 封面說成 1852 年 Paris–Boulogne 圖、把「1885」當 Ibry 的年份、把 Sergeev 寫成「俄國較早」、把 Petiet 與凡爾賽事故寫成因果、斷言「因為 Tufte 才叫馬雷圖」
- 時間軸向（橫或縱）沒標明；圖例壓住線的起點
- 事故還原時把圖當成原因（R20）；從一張照片推論全國都還在用印本（R21）
- 放進授權有疑問的圖（R14），或複製 Commons 圖卻不標作者與授權
- 把 X 貼文當歷史或方法依據：它們只是個人說法

## Produce checklist

- [ ] 故事句：「這條路線上每一班車在每個時間到了哪裡」；先決定路線、方向、日期與資料來源
- [ ] 站點依實際距離排列；軸向（時間橫軸或縱軸）在軸標寫清楚
- [ ] 每班車一條線（到站→離站→下一站到站，水平段＝停站）；顏色或線型分類方向、車種、計畫對實際
- [ ] 標出超車點、交會點（站內或站間）、誤點擴大段、串車開始的站；單線路線標出可會車的站
- [ ] 圖說的時刻與位置寫精確值；圖面寫「約」時另附精確值；誤點寫「晚幾分鐘」與擴大的原因
- [ ] 太密就拆：全天總覽加放大圖，或依尖峰、方向、車種分圖
- [ ] 模擬圖標模擬、圖說結尾寫「數字虛構」；圖面不是中文時，圖說只描述圖面可見內容並註明語言（R1、R4 法文，R5–R8 德文，R14–R17 日文等），與頁面說明不一致時只說兩者不一致
- [ ] 工具誠實：素材包**沒有實測任何軟體**。素材包只說「試算表散佈圖加連線可做小規模版本」（未實測）；大量資料可用 D3（網頁畫圖程式庫，參考 Bostock 範例，GPL-3.0 授權）、gtfs-marey（MIT 授權）、gtfs-to-chart 等開源工具（只列連結，沒有試用）；Excel、Google 試算表、Python、R 的具體步驟素材包沒有查，這裡不寫
- [ ] 歷史說法用限定語（第 2–8 點）；不放 Commons 圖進對外文件，除非逐張標作者與授權（見下方圖檔段）；R14 不放

## 虛構 demo 資料

素材包沒有指定哪一份給 repo，也沒有「合併版」樣本；它的八份虛構資料各自對應一張模擬圖（S1–S8）、各附一支自檢腳本，所以本 repo **八組成對收錄**到 `examples/data/`（共 8 個 CSV＋8 支 selfcheck，與素材包逐位元相同）。素材包的檔名已經加了 `marey` 前綴（`sample-marey-s1-anatomy.csv` 這類），我檢查過 `examples/data/` 沒有同名檔，**不需改名**。每支 selfcheck 以 `CSV_NAME` 加 `Path(__file__)` 讀**明確檔名**（沒有萬用字元；可選 argv[1]），時刻一律用精確分數（Fraction）計算；使用時也請用明確檔名，不要用 `sample-*.csv`。每個 CSV 第一行是 `#` 開頭的說明行（pandas 用 `comment='#'`），第二行是欄位名，每列 `data_status` 都寫「虛構資料，數字未核」。

| 檔案 | 對應圖 | 內容 |
|---|---|---|
| `sample-marey-s1-anatomy.csv` | S1 解剖 | 101 次下行、102 次上行；12 列；站點甲 0、乙 6、丙 9、丁 20、戊 24、己 35 公里 |
| `sample-marey-s2-local-vs-express.csv` | S2 | 普通 201、快車 301、201-nowait（不待避的對照）；14 列 |
| `sample-marey-s3-single-track-meet.csv` | S3（審稿外觀修正版） | 401、402、402-nowait（不等就開的對照）；15 列 |
| `sample-marey-s4-plan-vs-actual.csv` | S4 | plan 與 actual 兩線；12 列 |
| `sample-marey-s5-bus-bunching.csv` | S5 | bus1–bus5、第 0–12 站；65 列；arrive_min／depart_min 保留 6 位小數 |
| `sample-marey-s6-misread-equal-spacing.csv` | S6 | 601 次；站點 0、2、4、18、20、30 公里；6 列 |
| `sample-marey-s7-too-dense-zoom.csv` | S7 | 每班一列共 284 列；欄位另有 direction、kind、stops、in_zoom |
| `sample-marey-s8-steps.csv` | S8（審稿外觀修正版） | 501、502；甲到丁四站；8 列 |

欄位（素材包第 12 節）：S1–S4、S6、S8 與 S5 共 10 欄：group、train、seq（沿行駛方向第幾站，0 起）、station、km（距甲站公里）、arrive、depart（HH:MM 或 HH:MM:SS，起點沒有 arrive、終點沒有 depart）、arrive_min、depart_min（從 00:00 起算的分鐘）、data_status；S7 共 9 欄：group、train、direction（down／up）、kind（local／express）、stops、first_depart_min、last_arrive_min、in_zoom（1＝放大圖挑出的班次）、data_status。

我用 pandas／numpy／fractions **獨立重算**（讀 CSV 時用 `comment='#'`；以實際計數為準）；**與素材包敘述、selfcheck 逐項一致，沒有發現素材包文字與 CSV 不一致**：

- **S1**：101 與 102 只交叉一次，06:24:30、21.5 公里（丁站與戊站之間）；101 次丁站停 06:22–06:23
- **S2**：301 與 201 只交叉一次，07:24:00、20 公里（丁站）；301 與 201-nowait 交叉在 07:25:00、22 公里；301 時速 120 公里、201 各段 60 公里；己站 07:31:30 對 07:41，差 9.5 分鐘
- **S3**：401 與 402 只在戊站（24 公里）08:27 與 08:28 之間重合；401 與 402-nowait 只交叉一次，08:23:30、20.5 公里；402 在戊站等 9 分鐘
- **S4**：到站晚 1、2、7、7、7；離站晚（甲、乙、丙、丁、戊）0、2、4、7、7；停站多出 乙 +1、丙 +2；行駛多出 甲→乙 +1、丙→丁 +3；總計 7，丙站停站加丙到丁 5，占 71.4%
- **S5**：3→4 號車相隔 5.0、4.5、3.95、3.37、2.77、2.15、1.5、0.81、0.2、0.2、0.2、0.2、0.2，第 7 站首次小於 1；2→3 號車 11.0→16.13；**4→5 號車 8.0→最大 11.18（第 8 站）→9.76**；程式的 g（到站減前車離站）3→4 號車第 0 站 4.17、第 7 站起轉為負；3 號車第 0 站離站 17:19:50、4 號車 17:24:20，5 號車 18:04:48 到第 12 站；第 8–12 站 4 號車離站都比 3 號車晚 0.200
- **S6**：各段 2、2、14、2、10 公里＝2、2、14、2、10 分鐘，時速都是 60；等距視覺斜率 1／2、1／2、1／14、1／2、1／10，最平的是丙→丁
- **S7**：284＝普通 218（下行 109、上行 109）＋快車 66（下行 33、上行 33）；放大圖 16（普通 12＋快車 4，全部下行），占 5.6%；普通車每 10 分鐘、快車每 30 分鐘一班；同時在線最多 10 班
- **S8**：501 與 502 只交叉一次，10:13:30、11.5 公里
- **圖與腳本的實跑**：selfcheck 8 支都在暫存資料夾與 `examples/data/` 各實跑一次，結束碼 0、各輸出一行「OK」。`draw_marey.py` 預設輸出到**它自己旁邊的 `out/`**（不會寫進 teach-viz），並另寫 `sim_facts.json`；`export_samples.py` 預設寫回它自己所在的資料夾，且需要與 `draw_marey.py` 同一資料夾（它載入該檔取資料）。我只在暫存資料夾執行並用 `--outdir /tmp/…` 指定輸出，8 張模擬圖與素材包 `images/` 逐位元相同（`cmp`，含審稿修正的 S3、S8），匯出的 8 個 CSV 與素材包逐位元相同。兩支腳本**本 repo 不收**，只在 `ATTRIBUTION.md` 註明

## 參考連結（可點；皆出自素材包 sources.txt 且標可開；R14 不連結）

- 條目與定義：https://en.wikipedia.org/wiki/Time%E2%80%93distance_diagram 、https://en.wikipedia.org/wiki/%C3%89tienne-Jules_Marey 、https://de.wikipedia.org/wiki/Bildfahrplan 、https://ja.wikipedia.org/wiki/%E3%83%80%E3%82%A4%E3%83%A4%E3%82%B0%E3%83%A9%E3%83%A0 、https://zh.wikipedia.org/wiki/%E8%BF%90%E8%A1%8C%E5%9B%BE （會重新導向到「趨勢圖」，不是列車運行圖）、https://en.wikipedia.org/wiki/Train_timetable （頁名現已改為 Public transport timetable）、https://en.wikipedia.org/wiki/Bus_bunching 、https://en.wikipedia.org/wiki/Andria%E2%80%93Corato_train_collision
- 原始文獻與歷史：Marey《La Méthode Graphique》第二章（法文維基文庫）https://fr.wikisource.org/wiki/La_m%C3%A9thode_graphique/II ；Friendly 時間軸 http://euclid.psych.yorku.ca/SCS/Gallery/timelines.html 、里程碑第 6 節 http://euclid.psych.yorku.ca/SCS/Gallery/milestone/sec6.html ；datavis.ca 里程碑（含 Sergeev 條目；網址帶重複的 index.php，仍能開）https://www.datavis.ca/milestones/index.php/index.php?group=1850%2B ；Chartography.net https://www.chartography.net/p/charts-follow-chaos ；Rendgen https://sandrarendgen.wordpress.com/2019/03/15/data-trails-from-paris-with-love/ （素材包當天用命令列重測被擋，但審後稿的程式開啟與網頁抓取工具都讀得到全文，仍標可開）；里昂第一大學電子文件 https://esb.univ-lyon1.fr/pdf/UsagersLigne32.pdf ；Tufte 書籍頁 https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/ ；美國專利審理委員會公開證物（含 Tufte 書頁）https://ptabdata.blob.core.windows.net/files/2016/IPR2016-01237/Exhibit-1018.pdf ；視覺化史料清單 https://github.com/infowetrust/history/blob/master/originalWorks.csv
- 工具與實作範例：Bostock「Marey's Trains II」https://gist.github.com/mbostock/5544621 （bl.ocks 舊網址 https://bl.ocks.org/mbostock/5544621 會轉到 Gist；GPL-3.0）；Jake Coppinger Sydney 公車 https://jakecoppinger.com/2022/11/visualising-sydney-bus-congestion-with-marey-charts/ 、https://github.com/jakecoppinger/sydney-transit-graph ；美國交通研究資料庫論文 https://trid.trb.org/view/1217341 ；gtfs-marey（MIT）https://github.com/MobilityStuff/gtfs-marey ；gtfs-to-chart https://github.com/BlinkTagInc/gtfs-to-chart ；Plugboard 公車總站範例 https://docs.plugboard.dev/latest/examples/demos/transport/002_bus_terminal/bus-terminal/
- 台灣：台灣鐵路／軌道運行圖 https://tradiagram.com/ ；舊站 https://tradiagram.elvislo.tw/ （橫幅寫網域租約到 2026-09-23，已過期，隨時可能失效，**不當依據**）；billy1125（MIT，作者呂卓勳）https://github.com/billy1125/billy1125.github.io ；政府資料開放平臺鐵路時刻表 https://data.gov.tw/dataset/6138
- 圖庫分類：https://commons.wikimedia.org/wiki/Category:Graphic_timetables
- Commons 圖片頁（授權與作者見下方圖檔段）：R1 https://commons.wikimedia.org/wiki/File:Ibry%27s_Visual_Train_Schedule.png ；（已刪除的 R2 的來源頁）https://commons.wikimedia.org/wiki/File:PSM_V15_D338_Ibry_graphic_of_progress_of_trains_on_railways.jpg ；R3 https://commons.wikimedia.org/wiki/File:Diagram_showing_the_working_of_trains_between_Liverpool_and_Manchester.png ；R4 https://commons.wikimedia.org/wiki/File:Horaire_LEB_juin_1894.jpg ；R5 https://commons.wikimedia.org/wiki/File:Grafischer_Fahrplan_1899.jpg ；R6 https://commons.wikimedia.org/wiki/File:Graphischer_Fahrplan_Gro%C3%9Fherzoglich_Badische_Eisenbahnen.jpg ；R7 https://commons.wikimedia.org/wiki/File:Train_graph_Riesbahn_2005.svg ；R8 https://commons.wikimedia.org/wiki/File:Bildfahrplan_S28.png ；R9 https://commons.wikimedia.org/wiki/File:MBTA_Fitchburg_Line_chart.svg ；R10 https://commons.wikimedia.org/wiki/File:Bangalore_Outbound_Trains_Frequency_Chart.png ；R11 https://commons.wikimedia.org/wiki/File:Liding%C3%B6banan-grafisktidtabell2009-by-BIL.png ；R12 https://commons.wikimedia.org/wiki/File:Graphique_circulation.png ；R13 https://commons.wikimedia.org/wiki/File:Grafico_semplice_binario.jpg ；R15 https://commons.wikimedia.org/wiki/File:%E3%83%80%E3%82%A4%E3%83%A4%E3%82%B0%E3%83%A9%E3%83%A0_%E6%A8%99%E6%BA%96.png ；R16 https://commons.wikimedia.org/wiki/File:%E3%83%80%E3%82%A4%E3%83%A4%E3%82%B0%E3%83%A9%E3%83%A0_%E8%BF%BD%E3%81%84%E6%8A%9C%E3%81%8D.png ；R17 https://commons.wikimedia.org/wiki/File:%E3%83%80%E3%82%A4%E3%83%A4%E3%82%B0%E3%83%A9%E3%83%A0_%E3%81%99%E3%82%8C%E9%81%95%E3%81%84.png ；R18 https://commons.wikimedia.org/wiki/File:Local_service_graph.png ；R19 https://commons.wikimedia.org/wiki/File:Mixed_service_graph.png ；R20 https://commons.wikimedia.org/wiki/File:Andria%E2%80%93Corato_train_collision.svg ；R21 https://commons.wikimedia.org/wiki/File:Prints_of_Gapeka_2014_Inside_Cisomang_Station%27s_Train_Dispatcher_Room.jpg
- X 貼文（13 則，素材包用命令列只看得到網頁外框，內文是用 X 官方貼文讀取工具讀回，標「可開」；**只作連結、不當教學依據**，貼文只是個人說法）：見下方 X 段
- 查核限制（**未核；僅記名、不列連結，不是已驗證的來源**）：(1) Data Viz Catalogue 的 Marey chart 頁面——網站回覆查無此網址（頁面不存在）；(2) From Data to Viz 的 Marey 頁面——同樣頁面不存在；(3) Observable 的 Bostock「Marey's Trains」頁面與 (4) Observable 的 D3「Marey chart」頁面——請求過多，網站只回安全檢查頁，讀不到內容，**無法確認**；要引 Bostock 範例只引上面的 GitHub Gist。以上四頁都不當依據
- 連結統計：sources.txt 69 條（去重；檔案另有 8 行 `#` 說明）＝可開 65＋打不開 2＋無法確認 2。可開 65 條中 **64 條連結**（含 R2 的來源頁、bl.ocks 轉址、已過期的舊站〔註明不當依據〕與 13 則 X 貼文）；**刻意不連結的可開網址 1 條＝R14 的 Commons 頁面**（授權有效性無法證實）；打不開 2 條與無法確認 2 條只記名、未核（連結 64／刻意不連結 1／只記名 4）

## X 的情況

查詢時間：審稿以 X 平臺官方的貼文讀取功能在台北時間 2026-10-05 上午逐則讀回原文，核對作者、內容、發文日期；X 顯示的是世界標準時間，素材包已加 8 小時換算成台北時間。**繁體中文「馬雷圖」專帖：0 則**；中文「運行圖／列車運行圖」查到 46 筆，絕大多數是中國「實行新的列車運行圖」營運新聞（指營運計畫，不是圖表），只採用 1 則台灣原帖（第 8 則）；英文以 Marey chart、stringline、train graph 查，日文以ダイヤグラム查。**13 則外文原帖全部只放連結與摘要，僅轉載，不當歷史事實或方法依據**；這不代表 X 上沒有人談，只代表當時的查詢結果。

1. @staskulesh，2024-05-21 22:26：Marey 1885 年列車時刻圖在 Tufte 書中重印。https://x.com/staskulesh/status/1792924918356537639
2. @crispamares，2020-04-10 21:10：說這張圖其實是 Ibry 設計、原始想法可能來自俄國；「俄國」只是貼文轉述，不是 Sergeev 說法的獨立來源。https://x.com/crispamares/status/1248599297760911365
3. @A320Lga，2021-03-20 07:16（世界標準時間 03-19 23:16，換算後跨日）：說 stringline、string chart、marey chart 都是常見叫法；只能證明有人這樣稱呼，不是術語標準。https://x.com/A320Lga/status/1373050669607886848
4. @MBTA_CR，2019-09-19 21:21：說明服務規劃人員用的 string line chart（Marey diagram）；帳號顯示名稱為麻薩諸塞灣交通局通勤鐵路，但沒有認證標記，不視為官方說明。https://x.com/MBTA_CR/status/1174674832501420034
5. @TransSee，2020-12-20 21:17：營運圖可看出誤點、空檔與串車。https://x.com/TransSee/status/1340647583165902850
6. @kappyland，2025-12-18 11:31：把 57 路公車串車畫成 stringline 藝術。https://x.com/kappyland/status/2001495575271747958
7. @aussiewongm，2026-07-31 11:23：稱這種圖為 train graph 或 string line。https://x.com/aussiewongm/status/2083030843485020253
8. @nturail，2026-09-28 18:32：臺大鐵道暨火車研習社社課預告（2026-09-30 週三 19:00），講如何把表列式時刻表視覺化成列車運行圖；只是預告，沒有課程內容，不能當方法依據。https://x.com/nturail/status/2104519638642303345
9. @WalkAroundTokyo，2026-09-29 19:52：西武控股總部大樓外觀以列車運行圖為設計（日文）；是發文者自己的說法，僅轉載，無法證實。https://x.com/WalkAroundTokyo/status/2104902234517754156
10. @series_223，2026-10-04 08:00：貼文原文是「北陸新幹線金澤開業前」的北陸本線運行圖滿是紅色特急線（日文），不是「延伸通車前」；內容是發文者的觀感。https://x.com/series_223/status/2106535000896307357
11. @e_finder，2026-10-05 06:32（世界標準時間 10-04 22:32，換算後跨日）：單線運行圖交會的動腦謎題（日文）；貼文是導向部落格的謎題，曝光只有 6，**參考價值低，審稿人建議刪，終稿先保留並註明**，本檔只列入、不使用。https://x.com/e_finder/status/2106875007494426979
12. @navitimeRailfan，2026-10-01 17:00：帳號開設公告，提到 NAVITIME「ダイヤグラム時刻表」功能（日文）。https://x.com/navitimeRailfan/status/2105583510849270118
13. @SeasideExp，2025-12-11 12:20：堺市立圖書館提供昭和 4 年南海鐵道難波到和歌山市運行圖表的可讀解析度影像（日文）。https://x.com/SeasideExp/status/1998971093659639846

要寫「圖怎麼畫、怎麼讀」，仍以維基百科、datavis.ca、Rendgen、Chartography、素材包的 Commons 圖與模擬圖為主。

鄰居 pattern：`time-series-trend.md`（折線圖：一個指標隨時間，不是移動物體的位置）、`gantt-schedule.md`（甘特圖：工作起訖，沒有空間軸）、`small-multiples.md`（班次太密時依方向、車種拆成多張）、`control-chart.md`（管制圖／趨勢圖 run chart 與「运行图」撞名，看的是流程是否受控）、`slope-two-period.md`（坡度圖：兩期升降，與馬雷圖的速度斜率不同）；整個路網（縱軸排不出一維順序）改用地圖或流量地圖，本 repo 暫無流量地圖專檔（仍在缺口清單）、`kaplan-meier-survival.md`（時間到事件的群體存活曲線；馬雷圖是移動物體沿路線的位置）、`swimmer-plot.md`（游泳圖：縱軸是受試者清單、橫軸是自起點的時間；馬雷圖縱軸是實際距離）。

圖檔留在教圖／skill-pack（素材包 `images/`，28 張＝20 張真實／示意圖加 8 張模擬圖，與終稿使用的檔案 MD5 逐一一致〔我另外用 `cmp` 逐一對照教學稿資料夾的同名檔，28 張全部相同〕），本 repo **不複製**任何圖，只列連結與授權；對帳見 `ATTRIBUTION.md`。**Commons 圖是 R1、R3–R21 共 20 張（沒有 R2，編號不重排），各有個別作者與授權**，我另外用 Commons API（2026-10-05，台北）逐張查了 21 個檔案頁（含已刪除 R2 的來源頁）的授權簡稱、作者欄、尺寸與授權分類：授權簡稱與作者都與素材包相符（公有領域：R1、R3、R4、R7，另 R2 的來源頁；CC BY-SA 4.0：R5、R6、R15–R21；CC BY-SA 3.0：R8、R9、R10、R11、R13；CC BY-SA 2.5：R12），分類確認多重授權：R8（GFDL＋CC BY-SA 3.0／2.5／2.0／1.0）、R9、R11、R13 都有 GFDL；R10 只有 CC BY-SA 3.0、沒有 GFDL。兩點照實記：R10 的 API 作者欄是上傳帳號 PlaneMad（素材包寫作者是 Arun Ganesh、PlaneMad 上傳，作者署名以圖面為準，我沒有重讀頁面）；R14 的 API 授權簡稱是 CC BY 3.0，分類同時有 CC-BY-3.0、CC-BY-SA-3.0-migrated 與 GFDL，與素材包說的「授權欄與說明欄不一致」相符，這也是本檔不採用它的原因。R4 的 API 分類為 PD-old-70-expired，R1／R2 為 PD-old-100-expired；各圖的歷史來源說明（Ibry 設計、翻拍屬衍生等）我沒有逐頁重讀；使用時必須標作者與授權：CC BY-SA 要標示作者與授權、衍生作品用同樣授權；GFDL（GNU 自由文件授權）通常要求附授權全文或連結；公眾領域可自由使用。對外轉載前建議再確認各授權的要求。

- R1 Marey 書中 Paris 到 Lyon 列車圖（Ibry 方法；Commons 標 1878 年版第 20 頁，Tufte 圖說寫 1885 年版第 20 頁）：Commons 作者欄 Étienne-Jules Marey（設計 Ibry、出版 Marey），公有領域；歷史印刷品掃描。作者行要寫「Commons 作者欄 Marey；設計 Ibry、出版 Marey」
- R3 倫敦西北鐵路 Liverpool 到 Manchester 運行圖：L. & N. W. R.，公有領域；書本圖版掃描，轉載
- R4 瑞士 LEB 鐵路 1894 年運行圖：J. Chappuis（Archives LEB），公有領域；檔案館原件掃描，轉載；上傳者註明自己不是作者
- R5 聖哥達鐵路 1899 年運行圖、R6 巴登大公國鐵路 1906 年夏季運行圖：Hp.Baumeler（翻拍者），CC BY-SA 4.0；翻拍歷史時刻表，屬衍生作品，原作者頁面未載
- R7 德國 Riesbahn 運行圖（時間在縱軸）：Dealerofsalvation，公有領域
- R8 S28 與 S8 路線手繪運行圖：Fabian Lenzen，GFDL＋CC BY-SA 3.0／2.5／2.0／1.0 多重授權
- R9 麻薩諸塞灣交通局 Fitchburg 線平日運行圖：Pi.1415926535，CC BY-SA 3.0＋GFDL 雙重授權
- R10 Bangalore 外開列車運行圖：Arun Ganesh（Commons 帳號 PlaneMad 上傳），CC BY-SA 3.0；須保留圖面署名「Arun Ganesh, National Institute of Design Bangalore」與資料來源 indiarailinfo.com 並附頁面連結
- R11 瑞典 Lidingöbanan 輕軌運行圖（時間在縱軸）：BIL B I Larsson，CC BY-SA 3.0＋GFDL 雙重授權
- R12 法國虛構範例運行圖（Dijon 到 Chalon-sur-Saône）：G CHP，CC BY-SA 2.5
- R13 義大利單線區間運行圖：Horatius，GFDL＋CC BY-SA 3.0 雙重授權；「真實」只依 Commons 說明，僅轉載
- R14 JR 西日本奈良線運行圖局部：作者欄 w0746203-1；**授權有效性無法證實（見第 16 點），不建議放進對外 skill，本檔不連結**
- R15 日文示意 標準運行圖、R16 日文示意 超車、R17 日文示意 交會：Mtodo，CC BY-SA 4.0
- R18 只有普通車的運行圖、R19 快慢車混跑的運行圖：Hemmers，CC BY-SA 4.0
- R20 Andria–Corato 相撞事故運行圖：Phoenix7777，CC BY-SA 4.0
- R21 印尼車站調度室牆上的運行圖印本：NFarras（Naufal Farras），CC BY-SA 4.0
- S1 解剖、S2 普通車與快車、S3 單線交會、S4 計畫對實際、S5 公車串車、S6 等距排站的誤讀、S7 班次太密要拆圖、S8 製作步驟：素材包自畫的**模擬圖**，虛構資料、數字未核，無外部授權限制，右下角有浮水印「模擬｜範例數字未核（虛構資料）」；其中 S3、S8 是審稿人的外觀修正圖（S3 圖例改放座標軸下方、S8 浮水印下移；圖說與數字沒變），`draw_marey.py` 已併入修正
- 版權所有、未見轉載許可的圖：本包 28 張**沒有**頁面載明版權所有的圖（20 張 Commons 圖都有授權標示，其中 R14 的有效性存疑；8 張自繪）；Bostock 範例（GPL-3.0）、gtfs-marey（MIT）、billy1125 專案（MIT）、政府資料開放平臺鐵路時刻表只放連結，沒有複製其內容或圖；Chartography.net、Rendgen 部落格、Tufte 書頁只引述與連結，不轉載圖。
