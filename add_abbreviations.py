#!/usr/bin/env python3
"""
为教材中的英文缩写添加英文全称和中文全称注释
格式：缩写 [English Full Name, 中文全称]
只在每个文件中第一次出现时添加
"""
import re
import os
import glob

# 缩写映射表：缩写 -> (英文全称, 中文全称)
ABBREVIATIONS = {
    # 通用工具与赛事
    "SPSS": ("Statistical Package for the Social Sciences", "统计产品与服务解决方案"),
    "MCM": ("Mathematical Contest in Modeling", "美国大学生数学建模竞赛"),
    "ICM": ("Interdisciplinary Contest in Modeling", "跨学科建模竞赛"),
    "PDF": ("Portable Document Format", "便携式文档格式"),
    "CSV": ("Comma-Separated Values", "逗号分隔值文件"),
    "SQL": ("Structured Query Language", "结构化查询语言"),
    "CPU": ("Central Processing Unit", "中央处理器"),
    "LED": ("Light Emitting Diode", "发光二极管"),
    "LCD": ("Liquid Crystal Display", "液晶显示器"),
    "BMI": ("Body Mass Index", "身体质量指数"),
    "ERAS": ("Enhanced Recovery After Surgery", "加速康复外科"),

    # 人工智能与机器学习
    "AI": ("Artificial Intelligence", "人工智能"),
    "ML": ("Machine Learning", "机器学习"),
    "DL": ("Deep Learning", "深度学习"),
    "NLP": ("Natural Language Processing", "自然语言处理"),
    "NLTK": ("Natural Language Toolkit", "自然语言工具包"),
    "SVM": ("Support Vector Machine", "支持向量机"),
    "SVC": ("Support Vector Classification", "支持向量分类"),
    "SVR": ("Support Vector Regression", "支持向量回归"),
    "KNN": ("K-Nearest Neighbors", "K近邻算法"),
    "RF": ("Random Forest", "随机森林"),
    "GBDT": ("Gradient Boosting Decision Tree", "梯度提升决策树"),
    "XGBoost": ("eXtreme Gradient Boosting", "极端梯度提升"),
    "LSTM": ("Long Short-Term Memory", "长短期记忆网络"),
    "MLP": ("Multi-Layer Perceptron", "多层感知机"),
    "RBF": ("Radial Basis Function", "径向基函数"),
    "BP": ("Back Propagation", "反向传播"),
    "CNN": ("Convolutional Neural Network", "卷积神经网络"),
    "RNN": ("Recurrent Neural Network", "循环神经网络"),
    "GAN": ("Generative Adversarial Network", "生成对抗网络"),
    "SHAP": ("SHapley Additive exPlanations", "沙普利加性解释"),
    "TCN": ("Temporal Convolutional Network", "时间卷积网络"),
    "MMoE": ("Multi-gate Mixture-of-Experts", "多门控专家混合模型"),
    "VADER": ("Valence Aware Dictionary and sEntiment Reasoner", "情感感知词典与情感推理器"),
    "RANSAC": ("Random Sample Consensus", "随机抽样一致性"),

    # 统计检验与差异比较
    "ANOVA": ("Analysis of Variance", "方差分析"),
    "ANCOVA": ("Analysis of Covariance", "协方差分析"),
    "MANOVA": ("Multivariate Analysis of Variance", "多元方差分析"),
    "HSD": ("Honestly Significant Difference", "真实显著差异"),
    "TOST": ("Two One-Sided Tests", "双单侧检验"),
    "t-test": ("Student's t-test", "t检验"),
    "F-test": ("F-test", "F检验"),
    "chi-square": ("Chi-Square Test", "卡方检验"),
    "KW": ("Kruskal-Wallis", "克鲁斯卡尔-沃利斯检验"),

    # 回归分析
    "OLS": ("Ordinary Least Squares", "普通最小二乘法"),
    "GLM": ("Generalized Linear Model", "广义线性模型"),
    "GEE": ("Generalized Estimating Equations", "广义估计方程"),
    "HLM": ("Hierarchical Linear Model", "分层线性模型"),
    "PLS": ("Partial Least Squares", "偏最小二乘法"),
    "MLE": ("Maximum Likelihood Estimation", "最大似然估计"),
    "VIF": ("Variance Inflation Factor", "方差膨胀因子"),
    "AIC": ("Akaike Information Criterion", "赤池信息准则"),
    "BIC": ("Bayesian Information Criterion", "贝叶斯信息准则"),
    "ICC": ("Intraclass Correlation Coefficient", "组内相关系数"),
    "IRR": ("Incidence Rate Ratio", "发生率比"),
    "EPV": ("Events Per Variable", "每变量事件数"),
    "ZIP": ("Zero-Inflated Poisson", "零膨胀泊松回归"),
    "ZINB": ("Zero-Inflated Negative Binomial", "零膨胀负二项回归"),
    "ZPRED": ("Z-score of Predicted Values", "预测值标准化残差"),
    "ZRESID": ("Z-score of Residuals", "残差标准化得分"),
    "RCS": ("Restricted Cubic Spline", "限制性立方样条"),
    "LOESS": ("Locally Estimated Scatterplot Smoothing", "局部估计散点平滑"),
    "GAM": ("Generalized Additive Model", "广义可加模型"),

    # 相关与降维
    "PCA": ("Principal Component Analysis", "主成分分析"),
    "CCA": ("Canonical Correlation Analysis", "典型相关分析"),
    "LDA": ("Linear Discriminant Analysis", "线性判别分析"),
    "QDA": ("Quadratic Discriminant Analysis", "二次判别分析"),
    "RDA": ("Redundancy Analysis", "冗余分析"),
    "MDS": ("Multidimensional Scaling", "多维标度分析"),
    "SVD": ("Singular Value Decomposition", "奇异值分解"),
    "DBSCAN": ("Density-Based Spatial Clustering of Applications with Noise", "基于密度的噪声应用空间聚类"),
    "KMO": ("Kaiser-Meyer-Olkin", " Kaiser-Meyer-Olkin检验"),
    "PAF": ("Principal Axis Factoring", "主轴因子法"),
    "EFA": ("Exploratory Factor Analysis", "探索性因子分析"),
    "CFA": ("Confirmatory Factor Analysis", "验证性因子分析"),
    "SEM": ("Structural Equation Model", "结构方程模型"),
    "AVE": ("Average Variance Extracted", "平均方差提取量"),
    "CR": ("Composite Reliability", "组合信度"),
    "CFI": ("Comparative Fit Index", "比较拟合指数"),
    "TLI": ("Tucker-Lewis Index", "塔克-刘易斯指数"),
    "RMSEA": ("Root Mean Square Error of Approximation", "近似误差均方根"),
    "SRMR": ("Standardized Root Mean Square Residual", "标准化残差均方根"),
    "CITC": ("Corrected Item-Total Correlation", "校正项总计相关性"),
    "CVI": ("Content Validity Index", "内容效度指数"),
    "AMOS": ("Analysis of Moment Structures", "矩结构分析"),
    "BFGS": ("Broyden-Fletcher-Goldfarb-Shanno", "拟牛顿优化算法"),
    "FDR": ("False Discovery Rate", "错误发现率"),
    "BH": ("Benjamini-Hochberg", "本雅明尼-霍赫贝格方法"),

    # 综合评价
    "AHP": ("Analytic Hierarchy Process", "层次分析法"),
    "FAHP": ("Fuzzy Analytic Hierarchy Process", "模糊层次分析法"),
    "TOPSIS": ("Technique for Order Preference by Similarity to an Ideal Solution", "逼近理想解排序法"),
    "VIKOR": ("VlseKriterijumska Optimizacija I Kompromisno Resenje", "多准则妥协解排序法"),
    "DEA": ("Data Envelopment Analysis", "数据包络分析"),
    "DMU": ("Decision Making Unit", "决策单元"),
    "CRITIC": ("Criteria Importance Through Intercriteria Correlation", "基于指标相关性的权重确定法"),
    "EWM": ("Entropy Weight Method", "熵权法"),
    "BWM": ("Best-Worst Method", "最优最劣方法"),
    "DEMATEL": ("Decision Making Trial and Evaluation Laboratory", "决策试验与评价实验室法"),
    "ISM": ("Interpretive Structural Modeling", "解释结构模型"),
    "MICMAC": ("Matrice d'Impacts Croisés Multiplication Appliquée à un Classement", "交叉影响矩阵相乘法"),
    "RSR": ("Rank Sum Ratio", "秩和比法"),
    "RFM": ("Recency, Frequency, Monetary", "最近消费、消费频率、消费金额模型"),
    "SBM": ("Slack-Based Measure", "基于松弛变量的测度模型"),
    "SFA": ("Stochastic Frontier Analysis", "随机前沿分析"),
    "VRS": ("Variable Returns to Scale", "可变规模报酬"),
    "EFFCH": ("Efficiency Change", "效率变化"),
    "TECHCH": ("Technical Change", "技术变化"),
    "RI": ("Random Index", "随机一致性指标"),
    "OW": ("Ordered Weighted", "有序加权"),
    "BO": ("Bayesian Optimization", "贝叶斯优化"),
    "CV": ("Coefficient of Variation", "变异系数"),

    # 时间序列与计量经济
    "AR": ("Autoregressive", "自回归"),
    "MA": ("Moving Average", "移动平均"),
    "ARMA": ("Autoregressive Moving Average", "自回归移动平均模型"),
    "ARIMA": ("Autoregressive Integrated Moving Average", "差分整合移动平均自回归模型"),
    "SARIMA": ("Seasonal Autoregressive Integrated Moving Average", "季节性差分自回归移动平均模型"),
    "ARCH": ("Autoregressive Conditional Heteroskedasticity", "自回归条件异方差"),
    "GARCH": ("Generalized Autoregressive Conditional Heteroskedasticity", "广义自回归条件异方差"),
    "ACF": ("Autocorrelation Function", "自相关函数"),
    "PACF": ("Partial Autocorrelation Function", "偏自相关函数"),
    "ADF": ("Augmented Dickey-Fuller", "增广迪基-富勒检验"),
    "KPSS": ("Kwiatkowski-Phillips-Schmidt-Shin", "KPSS平稳性检验"),
    "VAR": ("Vector Autoregression", "向量自回归模型"),
    "VECM": ("Vector Error Correction Model", "向量误差修正模型"),
    "ECM": ("Error Correction Model", "误差修正模型"),
    "DID": ("Difference-in-Differences", "双重差分法"),
    "PSM": ("Propensity Score Matching", "倾向得分匹配"),
    "RDD": ("Regression Discontinuity Design", "断点回归设计"),
    "IV": ("Instrumental Variable", "工具变量"),
    "TSLS": ("Two-Stage Least Squares", "两阶段最小二乘法"),
    "GMM": ("Generalized Method of Moments", "广义矩估计"),
    "SUR": ("Seemingly Unrelated Regression", "似不相关回归"),
    "FE": ("Fixed Effects", "固定效应"),
    "RE": ("Random Effects", "随机效应"),
    "TWFE": ("Two-Way Fixed Effects", "双向固定效应"),
    "ATT": ("Average Treatment effect on the Treated", "处理组平均处理效应"),
    "LM": ("Lagrange Multiplier", "拉格朗日乘子检验"),
    "LR": ("Likelihood Ratio", "似然比"),
    "RESET": ("Regression Equation Specification Error Test", "回归方程设定误差检验"),
    "FGLS": ("Feasible Generalized Least Squares", "可行广义最小二乘法"),
    "HC": ("Heteroskedasticity-Consistent", "异方差稳健"),
    "COD": ("Coefficient of Determination", "决定系数"),
    "SFA": ("Stochastic Frontier Analysis", "随机前沿分析"),
    "TFPW": ("Trend-Free Pre-Whitening", "无趋势预白化"),
    "GM": ("Grey Model", "灰色模型"),
    "AGO": ("Accumulating Generation Operator", "累加生成算子"),
    "MAE": ("Mean Absolute Error", "平均绝对误差"),
    "MAPE": ("Mean Absolute Percentage Error", "平均绝对百分比误差"),
    "RMSE": ("Root Mean Square Error", "均方根误差"),
    "MSE": ("Mean Squared Error", "均方误差"),

    # 空间计量
    "SAR": ("Spatial Autoregressive Model", "空间自回归模型"),
    "SDM": ("Spatial Durbin Model", "空间杜宾模型"),
    "SEM": ("Spatial Error Model", "空间误差模型"),
    "SLM": ("Spatial Lag Model", "空间滞后模型"),
    "SLX": ("Spatial Lag of X", "自变量空间滞后模型"),
    "SDEM": ("Spatial Durbin Error Model", "空间杜宾误差模型"),
    "SAC": ("Spatial Autoregressive Combined", "空间自回归组合模型"),
    "GIS": ("Geographic Information System", "地理信息系统"),
    "IDW": ("Inverse Distance Weighting", "反距离加权"),
    "LISA": ("Local Indicators of Spatial Association", "空间关联局部指标"),
    "GWR": ("Geographically Weighted Regression", "地理加权回归"),
    "MGWR": ("Multiscale Geographically Weighted Regression", "多尺度地理加权回归"),
    "GDP": ("Gross Domestic Product", "国内生产总值"),

    # 医学统计
    "OR": ("Odds Ratio", "比值比"),
    "RR": ("Relative Risk", "相对风险"),
    "HR": ("Hazard Ratio", "风险比"),
    "CI": ("Confidence Interval", "置信区间"),
    "AUC": ("Area Under the Curve", "曲线下面积"),
    "ROC": ("Receiver Operating Characteristic", "受试者工作特征曲线"),
    "CIF": ("Cumulative Incidence Function", "累积发生函数"),
    "CMH": ("Cochran-Mantel-Haenszel", "科克伦-曼特尔-亨塞尔检验"),
    "DCA": ("Decision Curve Analysis", "决策曲线分析"),
    "IDI": ("Integrated Discrimination Improvement", "综合判别改善指数"),
    "NRI": ("Net Reclassification Improvement", "净重新分类指数"),
    "KM": ("Kaplan-Meier", " Kaplan-Meier生存分析"),
    "SHR": ("Subdistribution Hazard Ratio", "子分布风险比"),
    "TP": ("True Positive", "真阳性"),
    "TN": ("True Negative", "真阴性"),
    "FP": ("False Positive", "假阳性"),
    "FN": ("False Negative", "假阴性"),
    "NB": ("Negative Binomial", "负二项"),
    "CT": ("Computed Tomography", "电子计算机断层扫描"),
    "VTE": ("Venous Thromboembolism", "静脉血栓栓塞症"),
    "SD": ("Standard Deviation", "标准差"),
    "SE": ("Standard Error", "标准误"),
    "IQR": ("Interquartile Range", "四分位距"),

    # Meta分析
    "SMD": ("Standardized Mean Difference", "标准化均值差"),
    "MD": ("Mean Difference", "均值差"),
    "RD": ("Risk Difference", "风险差"),
    "OR": ("Odds Ratio", "比值比"),
    "RR": ("Relative Risk", "相对风险"),
    "HR": ("Hazard Ratio", "风险比"),
    "CI": ("Confidence Interval", "置信区间"),
    "KS": ("Kolmogorov-Smirnov", "柯尔莫哥洛夫-斯米尔诺夫检验"),

    # 文本分析
    "TF": ("Term Frequency", "词频"),
    "IDF": ("Inverse Document Frequency", "逆文档频率"),
    "TF-IDF": ("Term Frequency-Inverse Document Frequency", "词频-逆文档频率"),
    "PMI": ("Pointwise Mutual Information", "点互信息"),
    "LDA": ("Latent Dirichlet Allocation", "隐含狄利克雷分配"),
    "CHI": ("Chi-Square", "卡方检验"),

    # 规划求解
    "LP": ("Linear Programming", "线性规划"),
    "MILP": ("Mixed Integer Linear Programming", "混合整数线性规划"),
    "DP": ("Dynamic Programming", "动态规划"),
    "TSP": ("Traveling Salesman Problem", "旅行商问题"),
    "GA": ("Genetic Algorithm", "遗传算法"),
    "PSO": ("Particle Swarm Optimization", "粒子群优化"),
    "SA": ("Simulated Annealing", "模拟退火"),
    "ACO": ("Ant Colony Optimization", "蚁群优化"),
    "DE": ("Differential Evolution", "差分进化"),
    "DEAP": ("Distributed Evolutionary Algorithms in Python", "Python分布式进化算法库"),
    "NSGA": ("Non-dominated Sorting Genetic Algorithm", "非支配排序遗传算法"),
    "IPM": ("Interior Point Method", "内点法"),
    "SSE": ("Sum of Squared Errors", "误差平方和"),
    "CVaR": ("Conditional Value at Risk", "条件风险价值"),
    "ODE": ("Ordinary Differential Equation", "常微分方程"),

    # 质量控制
    "QC": ("Quality Control", "质量控制"),
    "SPC": ("Statistical Process Control", "统计过程控制"),
    "UCL": ("Upper Control Limit", "上控制限"),
    "LCL": ("Lower Control Limit", "下控制限"),
    "USL": ("Upper Specification Limit", "上规格限"),
    "LSL": ("Lower Specification Limit", "下规格限"),
    "CPL": ("Capability Lower Limit", "下限过程能力"),
    "CPU": ("Capability Upper Limit", "上限过程能力"),
    "CPK": ("Process Capability Index", "过程能力指数"),
    "MR": ("Moving Range", "移动极差"),
    "GRR": ("Gauge Repeatability and Reproducibility", "量具重复性与再现性"),
    "DMAIC": ("Define, Measure, Analyze, Improve, Control", "定义、测量、分析、改进、控制"),
    "MTTF": ("Mean Time To Failure", "平均失效时间"),
    "AOI": ("Automated Optical Inspection", "自动光学检测"),
    "SMT": ("Surface Mount Technology", "表面贴装技术"),
    "ABC": ("Activity-Based Costing", "作业成本法"),
    "ALT": ("Accelerated Life Testing", "加速寿命试验"),
    "CL": ("Center Line", "中心线"),

    # 试验设计
    "DOE": ("Design of Experiments", "试验设计"),
    "CCD": ("Central Composite Design", "中心复合设计"),
    "BBD": ("Box-Behnken Design", "Box-Behnken设计"),
    "RSM": ("Response Surface Methodology", "响应面方法"),
    "PB": ("Plackett-Burman", "Plackett-Burman设计"),

    # 问卷研究
    "KANO": ("Kano Model", "狩野模型"),
    "NPS": ("Net Promoter Score", "净推荐值"),
    "CBC": ("Choice-Based Conjoint", "基于选择的联合分析"),
    "IDP": ("Independent Double Programming", "独立双项目编程"),
    "OPP": ("Opportunity", "机会"),
    "PMC": ("Product-Moment Correlation", "积差相关"),
    "PME": ("Partial Method of Equating", "部分等值法"),
    "EU": ("Expected Utility", "期望效用"),
    "UA": ("Usage Attitude", "使用态度"),
    "BPTO": ("Brand Price Trade-Off", "品牌价格权衡"),

    # 功效分析
    "GLM": ("General Linear Model", "一般线性模型"),

    # 其他
    "IQR": ("Interquartile Range", "四分位距"),
    "EWMA": ("Exponentially Weighted Moving Average", "指数加权移动平均"),
    "CVM": ("Cramér-von Mises", "Cramér-von Mises检验"),
    "RCA": ("Root Cause Analysis", "根本原因分析"),
    "SNA": ("Social Network Analysis", "社会网络分析"),
    "SIR": ("Susceptible-Infected-Recovered", "易感-感染-恢复模型"),
    "POR": ("Proportional Odds Ratio", "比例优势比"),
    "POT": ("Peaks Over Threshold", "超阈值峰值"),
    "PWH": ("Prais-Winsten Hatanaka", "Prais-Winsten-Hatanaka估计"),
    "LPI": ("Logistic Performance Index", "物流绩效指数"),
    "FGI": ("Forecasted Growth Index", "预测增长指数"),
    "FOI": ("Force of Infection", "感染力"),
    "EBC": ("Evidence-Based Classification", "循证分类"),
    "EBQ": ("Evidence-Based Quantification", "循证量化"),
    "EDA": ("Exploratory Data Analysis", "探索性数据分析"),
    "EEE": ("Energy, Environment, Economy", "能源-环境-经济"),
    "II": ("Interaction Index", "交互指数"),
    "NYT": ("New York Times", "纽约时报"),
    "CE": ("Cost-Effectiveness", "成本效果"),
    "AFC": ("Average Fixed Cost", "平均固定成本"),
    "ERR": ("Error Rate Ratio", "错误率比"),
    "WX": ("Weather X", "天气变量X"),
}

def add_abbreviation_notes(filepath):
    """为单个文件添加缩写注释，只在第一次出现时添加"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 记录已经添加过注释的缩写
    added = set()
    # 按缩写长度降序排列，避免短缩写先匹配（如AR先于ARIMA匹配）
    sorted_abbrs = sorted(ABBREVIATIONS.keys(), key=len, reverse=True)

    lines = content.split('\n')
    in_code_block = False
    modified = False

    for i, line in enumerate(lines):
        # 跟踪代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # 跳过链接和图片
        if 'http' in line or '![' in line:
            continue

        for abbr in sorted_abbrs:
            if abbr in added:
                continue
            # 使用前后瞻断言匹配，支持中英文边界
            # 前面不能是字母数字，后面不能是字母数字
            pattern = r'(?<![A-Za-z0-9])' + re.escape(abbr) + r'(?![A-Za-z0-9])'
            if re.search(pattern, lines[i]):
                full_en, full_zh = ABBREVIATIONS[abbr]
                replacement = f"{abbr} [{full_en}, {full_zh}]"
                # 只替换第一次出现
                lines[i] = re.sub(pattern, replacement, lines[i], count=1)
                added.add(abbr)
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return len(added)
    return 0


def main():
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    md_files = sorted(glob.glob(os.path.join(docs_dir, '*.md')))

    total_added = 0
    for md_file in md_files:
        filename = os.path.basename(md_file)
        count = add_abbreviation_notes(md_file)
        if count > 0:
            print(f"  {filename}: 添加了 {count} 个缩写注释")
            total_added += count

    print(f"\n总计: 处理了 {len(md_files)} 个文件，添加了 {total_added} 个缩写注释")


if __name__ == '__main__':
    main()
