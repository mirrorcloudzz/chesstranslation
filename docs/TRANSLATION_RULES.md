# 国际象棋中文翻译执行约定

本页汇总现有项目说明与2026-10-12、13用户确认规则，供 Git 同步后的工作接续。逐段订正仍以各书校对记录为准。最新具体用户决定优先；早期排版建议和历史技能快照不能覆盖后续决定。

## 修改与校样

- 区分“意见已记录”“权威稿已修改”“派生数据已同步”“PDF已更新”。日常校对不自动重排PDF。
- 原始PDF、扫描、原始OCR保留；人工校订另存。原书错谱与OCR错误分别记录，不静默改写作者观点。
- 保留稳定段号、来源页和合并单元映射，不能为排版方便重编号。
- 作者原注、纳恩编者注和译者注分别标识。不把用户提供的引擎判断写成独立验证结论。
- 根据上下文恢复段落及棋谱，不把分页当段落结束。图注信息不足时留空待校，不猜填。

## 常用术语与译名

| 英文或语境 | 已确认译法 |
| --- | --- |
| develop the pieces / development | 出子 |
| stalemate | 逼和；不与普通和棋或长将混用 |
| win / lose a piece | 得子／失子 |
| sacrifice | 弃子；具体可写弃兵、弃马等 |
| classic bishop sacrifice | 古典弃象 |
| positional | 优先“局面棋／局面棋的”，按语境调整，避免机械替换 |
| bishop move | 动象，不能写“象棋” |
| pawn move，非吃子语境 | 冲兵；向指定格走可写“冲起e4” |
| pawn offensive / pawn attack | 兵的攻击 |
| break，冲击兵链打开局面 | 冲兵突破 |
| pawn majority | 按所在翼写后翼多兵／王翼多兵 |
| material advantage | 子力优势 |
| mate in N moves | N步杀 |
| castle queenside | 长易位 |
| square | 格，如a8格 |
| blindfold simultaneous / display | 盲棋车轮战 |
| Philidor / Najdorf | 菲利道尔／纳道尔夫 |
| Evans Gambit | 伊文斯弃兵 |
| Nimzo-Indian Defence | 尼姆佐-印度防御；与1. e4 Nc6的尼姆佐维奇防御区分 |
| King's / Queen's Gambit Accepted | 王翼／后翼弃兵接受弃兵变例 |
| King's / Queen's Gambit Declined | 王翼／后翼弃兵拒弃兵变例 |

其他开局名称中的 Accepted、Declined 同样采用“接受弃兵变例”“拒弃兵变例”，普通动词按语境翻译。姓名沿用已确认的塔塔科维尔、布雷耶尔、马卡戈诺夫、泰曼诺夫、波戈留波夫、马洛契、齐果林；Hastings 为黑斯廷斯。

## 棋谱与棋图

棋谱用现代 SAN，例如 `1. Kf4`、`1... Kf6`、`2. Kg4 Kg6`，具体用户指定的局部格式另行保留。原书主线粗体层级保留，分析变化与普通行内招法使用正文字体，不加绿色底框。黑方省略号用三个英文句点。

完整例局图注说明形成局面的最后一步，短片段根据来源注明棋手及行棋方。图注去除 `!`、`?` 及组合，保留 `+`、`#`；正文评注符号保留。原书 `(D)` 须结合上下文核对，不能简单取图前最近招法。

当前《进攻的艺术》校样使用已核对扫描裁片；第四章部分原图只有半盘，应保留原范围。早期指导方案中的最终出版矢量重绘建议不作为当前校样的自动操作。图、图注、锚点及紧接的讲解尽量同页。

## 2026-10-18语言统稿补充

本书同一人物在正文、图注和索引中统一为：科勒、雷舍夫斯基、格利戈里奇、斯塔尔贝里、拉宾诺维奇、米泽斯、罗索利莫、武科维奇，以及D. 伯恩（与Burn的伯恩保留首字母区分）。这是本次同书一致性整理，不替代此前用户明确确认的译名规范。

`commitment`按语境表述作出的投入及其对后续选择造成的约束；`obligation`在这种棋理语境中可为局面约束，不机械直译成道德意义的承诺或义务。`tempo of the attack`与具体赢得的一先、动作所耗一步时间分别判断。作者和纳恩所说today/modern/recent等按其写作年代理解，避免让读者误以为是本次校对年份的新理论结论。

来源：[当前书说明](../translations/art_of_attack/README.md)、[用户订正](../translations/art_of_attack/translation/USER_CORRECTIONS.md)、[中局计划说明](../translations/chess_middlegame_planning/README.md)、[早期排版方案](../books/TRANSLATION_LAYOUT_GUIDE.md)。2026-10-16已将此前确认的术语与逐段订正应用至《进攻的艺术》当前稿及全书v2校样；《中局计划》第一版保持不变。
