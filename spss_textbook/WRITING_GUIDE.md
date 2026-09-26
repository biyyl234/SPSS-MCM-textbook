# SPSS数模美赛教材 - 写作规范（所有章节必须严格遵守）

## 一、文档结构

每个章节文件（chXX.tex）必须包含：
1. `\chapter{分类名称}` - 章节标题
2. `\begin{chapteroverview}...\end{chapteroverview}` - 本章导览框（分类是干啥的、美赛什么题型常用、学习路径建议）
3. `\section{基础级算法}` - 基础算法部分
4. 每个基础算法：`\basicalgo{{\starmark}算法名称}{label}` + 6个模块框
5. `\section{进阶级算法速览}` - 进阶算法部分
6. 每个进阶算法：`\advancedalgo{算法名称}{label}` + 1个algobrief框

## 二、可用的LaTeX命令和环境

### 章节结构命令
```latex
\basicalgo{{\starmark}算法名称}{unique_label}  % 基础算法，带星标
\basicalgo{算法名称}{unique_label}              % 基础算法，无星标
\advancedalgo{算法名称}{unique_label}           % 进阶算法
```
- label用英文小写+下划线，如 `linear_regression`，确保全文档唯一
- 星标算法（is_star=true）必须加 `{\starmark}` 前缀

### 六大模块环境（基础算法必须全部使用，顺序固定）
```latex
\begin{algointro}...\end{algointro}           % 一句话讲清
\begin{algoscene}...\end{algoscene}           % 美赛适用场景
\begin{algoprinciple}...\end{algoprinciple}   % 通俗原理
\begin{algosposs}...\end{algosposs}           % SPSS操作步骤
\begin{algoresult}...\end{algoresult}         % 结果怎么看
\begin{algonotes}...\end{algonotes}           % 注意事项&决策指引
```

### 进阶算法简洁框
```latex
\begin{algobrief}
\textbf{一句话}：...
\textbf{美赛场景区}：...
\textbf{核心原理}：...
\textbf{操作要点}：...
\textbf{结果关键}：...
\textbf{注意}：...
\end{algobrief}
```

### 本章导览框
```latex
\begin{chapteroverview}
\textbf{这个分类是干什么的？}
...
\textbf{美赛什么题型常用？}
...
\textbf{学习路径建议}
...
\end{chapteroverview}
```

## 三、写作风格要求

### 目标读者
大一学生，只有高中数学基础，可能没学过线性代数和概率论。

### 语言要求
- 像学长学姐带新手，亲切但不啰嗦
- 专业术语首次出现必须用通俗语言解释
- 多用生活类比（如"回归分析就像找最佳拟合线"）
- 关键公式、统计量名称、判断阈值要准确
- 每个模块内容充实但不冗余，基础算法每个模块3-8句话或3-6个要点

### 通俗原理模块特别要求
- 必须有生活类比
- 公式必须配文字说明每个符号的含义
- 不要堆砌公式，1-3个核心公式即可
- 用itemize分点说明

### SPSS操作步骤模块特别要求
- 具体到菜单路径，如"分析 → 回归 → 线性"
- 说明选什么变量、参数怎么填
- 基于案例数据中的默认参数（从JSON的params字段读取）
- 用enumerate编号步骤
- 如果SPSS原生不支持该算法（如某些高级计量方法），说明"在Dabbit AI SPSS工具箱中操作"或"通过SPSS的R/Python扩展实现"

### 结果怎么看模块特别要求
- 说明输出表格中每个关键指标的含义
- 给出判断阈值（如p>0.05表示什么）
- 说明怎么判断结果"好"或"坏"

### 注意事项模块特别要求
- 必须包含：什么时候用、什么时候不用
- 必须包含：至少2个常见坑
- 必须包含：和1-2个相似算法的区别

## 四、LaTeX特殊字符转义（非常重要！）

以下字符在LaTeX中有特殊含义，正文出现时必须转义：
- `%` → `\%`
- `&` → `\&`
- `#` → `\#`
- `_` → `\_`（但在数学公式$...$中不需要）
- `$` → `\$`（但用于数学环境时不转义）
- `{` `}` → `\{` `\}`
- `~` → `\textasciitilde`
- `^` → `\textasciicircum`
- `<` `>` 在正文中用 `\textless` `\textgreater`（数学公式中直接用）

中文标点不需要转义。数学公式用 `$...$` 行内或 `\[...\]` 行间。

## 五、数据来源

每个分类的数据文件在：
`C:\Users\biyyl234\Desktop\dabbit ai\spss_textbook\data\cat_XX_分类名.json`

JSON结构：
```json
{
  "category": "分类名",
  "chapter_num": N,
  "total": M,
  "basic_count": X,
  "advanced_count": Y,
  "star_algos": ["算法A", "算法B"],
  "cases": [
    {
      "algorithmName": "算法名",
      "params": {"参数名": "默认值", ...},
      "background": "案例背景描述",
      "report": "分析报告全文",
      "tables": [...],
      "category": "分类",
      "tier": "basic" 或 "advanced",
      "is_star": true 或 false,
      "seq": 序号
    }
  ]
}
```

必须读取对应JSON文件，基于其中的params（默认参数）、background（案例背景）、report（分析报告）来撰写内容，确保操作步骤和结果解读与实际案例一致。

## 六、输出要求

- 输出文件路径：`C:\Users\biyyl234\Desktop\dabbit ai\spss_textbook\chapters\chXX.tex`
- 文件编码：UTF-8
- 不需要写`\begin{document}`等，只写章节内容（会被main.tex的\input引入）
- 所有算法必须覆盖，不能遗漏
- 基础算法必须6个模块齐全
- 进阶算法用algobrief简洁框
- 写完后自查：算法数量是否完整、模块是否齐全、特殊字符是否转义
