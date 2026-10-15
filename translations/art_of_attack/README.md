# Art of Attack in Chess — 翻译资料

日期：2026-10-01。当前阶段：开篇至第五章末的中文初译与分段中英对照校样已完成，待用户校对。

已保存352张原页图、332张棋图裁片；已完成352/352页 OCR。OCR页覆盖完整。

入口：[按目录阅读英文 OCR](OCR_INDEX.md) · [准备记录与注意事项](PREPARATION_NOTES.md) · [棋图浏览页](qa/figure_gallery.html) · [检查报告](qa/validation.json)。

按目录独立保存了编者序、导言、12章、符号说明和两份索引，另保存封面封底与目录的 OCR。每一部分都有 Markdown、TXT 与坐标 JSON。

原始OCR保持不变，不等同于英文校订稿。封面、封底、目录、符号说明、编者序、导言及第一至第五章（原书第1—120页）已经对照扫描页整理，合并跨页句子，恢复棋子符号，并形成独立的校订英文和中文初译。第六章起仍处于未经逐句校勘的OCR准备阶段。

## 当前译稿与校样

- [开篇材料与编者序](translation/front_preface_v1.md)：FM-1—FM-12，PF-1—PF-6；PDF共3页。
- [导言](translation/introduction_v1.md)：IN-1—IN-46；PDF共10页，4幅棋图。
- [第一章](translation/ch01_v1.md)：CH1-1—CH1-160；PDF共19页，14幅棋图，3处纳恩编者脚注。
- [结构化译稿及原页溯源](translation/segments_v1.json)、[校样清单](translation/proof_manifest_v1.json)、[棋图锚点及图注](translation/figure_anchors_v1.json)。
- [棋谱检查](translation/chess_validation_v1.json)：35组实战与分析变化，共893个半回合，未发现非法走法；检查不含引擎评价，也不意味着原书所有分析结论都正确。
- [排版检查](translation/layout_validation_v1.json)：全32页已渲染检查；18幅图均与锚点、下一段同页，未发现页面边界溢出。

### 第二批：第二至第五章

- [第二章：攻击失去易位权利的王](translation/ch02_v1.md)：CH2-1—CH2-244，原书28—50页；校样33页、25图。
- [第三章：易位与攻击王城的一般问题](translation/ch03_v1.md)：CH3-1—CH3-115，原书51—65页；校样18页、8图。
- [第四章：将杀模式](translation/ch04_v1.md)：CH4-1—CH4-80，原书66—79页；校样19页、31图。
- [第五章：杀王焦点](translation/ch05_v1.md)：CH5-1—CH5-434，原书80—120页；校样57页、44图。
- [第二批结构化译稿](translation/segments_ch02_05_v1.json)、[校样清单](translation/proof_manifest_ch02_05_v1.json)、[棋图锚点](translation/figure_anchors_ch02_05_v1.json)、[校订记录与原书疑点](translation/REVIEW_NOTES_ch02_05_v1.md)。
- [棋谱检查](translation/chess_validation_ch02_05_v1.json)：49组主线及选取的分析分支，1242个半回合，未发现非法走法或SAN差异；不是引擎评价，也不是对全部分析变化的穷尽验证。
- [排版检查](translation/layout_validation_ch02_05_v1.json)：全部127页已渲染并查看；873个中英对照单元完整，108图均与锚点及下一段同页，无文字边界溢出。

第二批校样沿用第一批的英文左栏、中文右栏和稳定段号。47幅匿名或教学示意图因没有完整对局信息而留空中文图注，不猜填；原图W/B及来源页仍保留。第四章原本只画半盘的示意图，保留原书范围。

桌面校样总文件夹保持原路径：`C:/Users/12059/Desktop/国际象棋中局计划_最新校样PDF`。旧书材料（含历史版本）已移入其中的`国际象棋中局计划`子文件夹；本书PDF保存于平行的`国际象棋进攻的艺术`子文件夹。迁移未改写旧书文件内容。

继续执行已确认的规则：用户通常提出修改时只更新/记录译稿，只有明确要求更新校样时才重新生成桌面PDF。原始OCR与图片仅作来源，不覆盖权威译稿。

2026-10-12用户确认的通用术语：`classic bishop sacrifice`统一译为“古典弃象”，已同步至棋书翻译skill，后续章节标题和正文均采用此译法。本次仅保存规范，未改动既有译稿或重新生成PDF；已有译稿中的“经典弃象”留待用户指定统一修改或更新时处理。

2026-10-12用户确认的软性术语规范：棋理语境中的`positional`优先译为“局面棋／局面棋的”，例如`positional ideas`为“局面棋思想”，`positional understanding`为“局面棋的理解”。除非导致明显不通顺，否则采用这一译法；例外按上下文调整并保留原意，不机械全局替换。已同步至棋书翻译skill，本次仅存档规范，既有译稿和PDF未更新。

待统一应用的逐段校对意见见[用户校对记录](translation/USER_CORRECTIONS.md)。2026-10-12已记录IN-40：`still accepted today`改为“直到本书写作时仍被接受”；本次未改稿、未重排PDF。

2026-10-12用户确认的通用开局命名规范：`King's Gambit Declined/Accepted`分别译为“王翼弃兵拒弃兵变例／王翼弃兵接受弃兵变例”，后翼弃兵同理。任意其他开局名称中的`Accepted`与`Declined`也分别使用“接受弃兵变例”与“拒弃兵变例”，除非用户明确另作说明；不套用于正文中的普通动词。已同步至棋书翻译skill，本次仅保存规范，既有译稿和PDF未更新。

2026-10-13用户确认的姓名规范：`Philidor`译为“菲利道尔”，`Najdorf`译为“纳道尔夫”，适用于正文、对局信息、图注及相关开局和变例名称。已同步至棋书翻译skill；旧译名列入[待统一修改记录](translation/USER_CORRECTIONS.md)，本次未改译稿或更新PDF。

2026-10-13用户确认的开局名称：`Evans Gambit`统一译为“伊文斯弃兵”，已同步至棋书翻译skill；既有“埃文斯弃兵”列入待统一修改记录，本次未改译稿或更新PDF。

2026-10-13用户确认的术语：`blindfold simultaneous`译为“盲棋车轮战”，`blindfold simultaneous display`同样采用；已同步至棋书翻译skill。CH2-32的“蒙目车轮战”已记为待统一修改，本次未改译稿或更新PDF。

其他两本待译书暂缓，既有资料与 Romanovsky 第一版成品保持不变。
