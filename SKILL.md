---
name: token-consumer-optimizer
description: "智能AI模型消费决策工具，帮助用户在众多AI模型中选择最经济、最适合的消费方案。通过实时比价、任务匹配和成本分析，让用户每一分钱都花在刀刃上。"
---

# Token消费优选师

**ID**: token-consumer-optimizer  
**版本**: 1.0.0  
**作者**: 张海洋 / 白泽  
**标签**: token, cost, optimization, ai, pricing  

---

## 简介

Token消费优选师是一款智能的AI模型消费决策工具，帮助用户在众多AI模型中选择最经济、最适合的消费方案。通过实时比价、任务匹配和成本分析，让用户每一分钱都花在刀刃上。

---

## 功能特性

### ✅ 智能比价引擎
- 实时对比9大主流模型价格
- 支持人民币/美元双币种显示
- 自动汇率换算

### ✅ 任务路由建议
- 根据任务类型推荐最优模型
- 6种预设任务场景
- 支持自定义预算级别

### ✅ 成本计算器
- 精确计算单次调用成本
- 支持批量成本预估
- 节省百分比分析

### ✅ 预算规划
- 月度预算分析
- 可调用次数预估
- 超预算预警

---

## 支持平台

| 模型 | 厂商 | 输入价格 | 输出价格 | 货币 |
|------|------|----------|----------|------|
| GPT-4o | OpenAI | $2.50 | $10.00 | USD |
| GPT-4o Mini | OpenAI | $0.15 | $0.60 | USD |
| Claude 3.5 Sonnet | Anthropic | $3.00 | $15.00 | USD |
| Kimi K2 | Moonshot | ¥0.15 | ¥0.60 | CNY |
| Kimi K2.5 | Moonshot | ¥0.50 | ¥2.00 | CNY |
| 文心一言4.0 | 百度 | ¥0.30 | ¥0.90 | CNY |
| 通义千问Max | 阿里 | ¥0.40 | ¥1.20 | CNY |
| 豆包Pro | 字节 | ¥0.08 | ¥0.32 | CNY |
| 豆包Lite | 字节 | ¥0.03 | ¥0.06 | CNY |

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/sealawyer2026/skill-token-consumer-optimizer.git
cd skill-token-consumer-optimizer

# 安装依赖
pip install -r requirements.txt
```

---

## 使用方法

### 1. 推荐最优模型

```bash
python main.py recommend --task code_generation --tokens 2000
```

**参数说明**:
- `--task`: 任务类型 (simple_qa/code_generation/document_processing/creative_writing/analysis/translation)
- `--tokens`: 输入token数
- `--budget`: 预算级别 (ultra_cheap/cheap/balanced/performance/ultra_performance)

### 2. 对比所有模型

```bash
python main.py compare --tokens 5000
```

### 3. 预算分析

```bash
python main.py budget --budget 1000 --daily-calls 50
```

### 4. 计算特定模型成本

```bash
python main.py calculate --model kimi-k2 --tokens 10000
```

### 5. JSON输出

所有命令都支持 `--json` 参数输出JSON格式，便于程序集成：

```bash
python main.py recommend --task simple_qa --tokens 1000 --json
```

---

## 使用示例

### 场景1: 代码生成任务

```bash
$ python main.py recommend --task code_generation --tokens 3000

📊 任务分析
   任务类型: code_generation
   输入Token: 3,000
   输出Token: 1,500
   预算级别: balanced

💡 推荐方案 (按性价比排序):
--------------------------------------------------------------------------------
🥇 #1 Kimi K2.5 (Moonshot)
    💰 预估成本: ¥0.0045 ($0.0006)
    📉 可节省: 95.2% (对比最贵方案)
    ✅ 推荐理由: 价格实惠，稳定可靠，响应快速
    📊 综合评分: 92.3/100

🥈 #2 GPT-4o (OpenAI)
    💰 预估成本: ¥0.0675 ($0.0094)
    📉 可节省: 28.6% (对比最贵方案)
    ✅ 推荐理由: 稳定可靠，响应快速
    📊 综合评分: 88.1/100
```

### 场景2: 长文档处理

```bash
$ python main.py recommend --task document_processing --tokens 100000

💡 使用 Kimi K2 处理10万token文档，比GPT-4o节省约 95% 成本！
```

### 场景3: 月度预算规划

```bash
$ python main.py budget --budget 500 --daily-calls 100 --tokens 2000

📊 预算分析报告
   月度预算: ¥500.00
   预估月调用: 3,000 次

💰 各模型月度成本:
--------------------------------------------------------------------------------
豆包Lite            ¥5.40        ✅ 支持
豆包Pro             ¥28.80       ✅ 支持
Kimi K2             ¥13.50       ✅ 支持
Kimi K2.5           ¥45.00       ✅ 支持
GPT-4o Mini         ¥38.88       ✅ 支持
文心一言4.0         ¥81.00       ✅ 支持
通义千问Max         ¥108.00      ✅ 支持
Claude 3.5 Sonnet   ¥1,296.00    ❌ 超预算
GPT-4o              ¥1,458.00    ❌ 超预算
```

---

## 任务类型说明

| 任务类型 | 说明 | 推荐模型 |
|----------|------|----------|
| simple_qa | 简单问答 | 豆包Lite, GPT-4o Mini, Kimi K2 |
| code_generation | 代码生成 | GPT-4o, Claude 3.5, Kimi K2.5 |
| document_processing | 长文档处理 | Kimi K2, Claude 3.5, 豆包Pro |
| creative_writing | 创意写作 | Claude 3.5, GPT-4o, 豆包Pro |
| analysis | 数据分析 | GPT-4o, Kimi K2.5, Claude 3.5 |
| translation | 翻译任务 | GPT-4o, Kimi K2, 豆包Pro |

---

## Python API

```python
from optimizer import TokenConsumerOptimizer, BudgetLevel

# 创建优化器
optimizer = TokenConsumerOptimizer()

# 推荐模型
recommendations = optimizer.recommend(
    task_type="code_generation",
    input_tokens=3000,
    budget_level=BudgetLevel.BALANCED
)

# 获取最佳推荐
top = recommendations[0]
print(f"推荐模型: {top.model.name}")
print(f"预估成本: ¥{top.total_cost_cny:.4f}")
print(f"推荐理由: {top.reason}")

# 计算特定模型成本
cost_cny, cost_usd = optimizer.calculate_cost("kimi-k2", 10000)
print(f"Kimi K2 处理1万token成本: ¥{cost_cny:.4f}")

# 预算分析
analysis = optimizer.analyze_budget(
    monthly_budget_cny=1000,
    daily_calls=50,
    avg_input_tokens=2000
)
```

---

## 价格数据更新

价格数据存储在 `price_data.json` 中，包含:
- 各模型实时价格
- 汇率信息
- 任务类型映射

定期更新价格数据以获得最准确的推荐。

---

## 技术架构

```
skill-token-consumer-optimizer/
├── main.py              # CLI入口
├── optimizer.py         # 核心推荐引擎
├── price_data.json      # 价格数据库
├── tests/               # 测试套件
├── SKILL.md             # 技能文档
└── README.md            # 使用说明
```

---

## 路线图

- [x] v1.0.0 - 基础比价功能
- [ ] v1.1.0 - 接入更多国产模型
- [ ] v1.2.0 - API批量优化建议
- [ ] v1.3.0 - 实时价格爬虫
- [ ] v2.0.0 - 企业级消费管控

---

## 相关项目

- [Token Master](https://clawhub.ai/sealawyer2026/token-economy-master) - Token压缩优化
- [Skill Self-Optimizer](https://clawhub.ai/sealawyer2026/skill-self-optimizer) - 技能自优化

---

## 许可证

MIT License

---

## 联系我们

- GitHub: https://github.com/sealawyer2026/skill-token-consumer-optimizer
- ClawHub: https://clawhub.ai/sealawyer2026/token-consumer-optimizer
