#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token消费优选师 - 核心推荐引擎
帮助用户选择最经济的AI模型消费方案
"""

import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class BudgetLevel(Enum):
    """预算级别"""
    ULTRA_CHEAP = "ultra_cheap"      # 极致省钱
    CHEAP = "cheap"                  # 经济型
    BALANCED = "balanced"            # 平衡型
    PERFORMANCE = "performance"      # 性能型
    ULTRA_PERFORMANCE = "ultra_performance"  # 极致性能
    CREATIVE = "creative"            # 创意型


@dataclass
class ModelInfo:
    """模型信息"""
    id: str
    name: str
    provider: str
    input_price: float
    output_price: float
    currency: str
    strengths: List[str]
    context_length: int
    speed: str
    reliability: float


@dataclass
class Recommendation:
    """推荐结果"""
    model: ModelInfo
    estimated_input_cost: float
    estimated_output_cost: float
    total_cost_cny: float
    total_cost_usd: float
    savings_percent: float
    reason: str
    score: float


class TokenConsumerOptimizer:
    """Token消费优选师"""
    
    USD_TO_CNY = 7.20  # 美元兑人民币汇率
    
    def __init__(self, price_data_path: str = "price_data.json"):
        """初始化"""
        self.models: Dict[str, ModelInfo] = {}
        self.task_types: Dict = {}
        self.load_data(price_data_path)
    
    def load_data(self, path: str):
        """加载价格数据"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载模型信息
            for m in data.get('models', []):
                self.models[m['id']] = ModelInfo(
                    id=m['id'],
                    name=m['name'],
                    provider=m['provider'],
                    input_price=m['input_price'],
                    output_price=m['output_price'],
                    currency=m['currency'],
                    strengths=m['strengths'],
                    context_length=m['context_length'],
                    speed=m['speed'],
                    reliability=m['reliability']
                )
            
            # 加载任务类型映射
            self.task_types = data.get('task_type_mapping', {})
            
        except FileNotFoundError:
            raise FileNotFoundError(f"价格数据文件未找到: {path}")
        except json.JSONDecodeError:
            raise ValueError(f"价格数据文件格式错误: {path}")
    
    def to_cny(self, amount: float, currency: str) -> float:
        """转换为人民币"""
        if currency == "USD":
            return amount * self.USD_TO_CNY
        return amount
    
    def to_usd(self, amount: float, currency: str) -> float:
        """转换为美元"""
        if currency == "CNY":
            return amount / self.USD_TO_CNY
        return amount
    
    def calculate_cost(
        self, 
        model_id: str, 
        input_tokens: int, 
        output_tokens: Optional[int] = None
    ) -> Tuple[float, float]:
        """
        计算调用成本
        
        Args:
            model_id: 模型ID
            input_tokens: 输入token数
            output_tokens: 输出token数 (默认=input_tokens//2)
        
        Returns:
            (人民币成本, 美元成本)
        """
        if model_id not in self.models:
            raise ValueError(f"未知模型: {model_id}")
        
        model = self.models[model_id]
        output_tokens = output_tokens or input_tokens // 2
        
        # 计算原始货币成本 (每1M tokens)
        input_cost = (input_tokens / 1_000_000) * model.input_price
        output_cost = (output_tokens / 1_000_000) * model.output_price
        total_cost = input_cost + output_cost
        
        # 转换为人民币和美元
        if model.currency == "USD":
            cost_cny = total_cost * self.USD_TO_CNY
            cost_usd = total_cost
        else:
            cost_cny = total_cost
            cost_usd = total_cost / self.USD_TO_CNY
        
        return cost_cny, cost_usd
    
    def recommend(
        self,
        task_type: str,
        input_tokens: int,
        output_tokens: Optional[int] = None,
        budget_level: BudgetLevel = BudgetLevel.BALANCED,
        preferred_currency: str = "CNY"
    ) -> List[Recommendation]:
        """
        推荐最优模型
        
        Args:
            task_type: 任务类型 (simple_qa/code_generation/document_processing等)
            input_tokens: 预计输入token数
            output_tokens: 预计输出token数
            budget_level: 预算级别
            preferred_currency: 首选货币 (CNY/USD)
        
        Returns:
            推荐列表 (按性价比排序)
        """
        output_tokens = output_tokens or input_tokens // 2
        
        # 获取该任务类型推荐的模型
        task_config = self.task_types.get(task_type, {})
        recommended_model_ids = task_config.get('recommended_models', list(self.models.keys()))
        
        recommendations = []
        baseline_cost = None
        
        for model_id in recommended_model_ids:
            if model_id not in self.models:
                continue
            
            model = self.models[model_id]
            cost_cny, cost_usd = self.calculate_cost(model_id, input_tokens, output_tokens)
            
            # 计算预估输入/输出成本
            input_cost = (input_tokens / 1_000_000) * model.input_price
            output_cost = (output_tokens / 1_000_000) * model.output_price
            
            # 设置基准成本 (最贵的作为基准)
            if baseline_cost is None or cost_cny > baseline_cost:
                baseline_cost = cost_cny
            
            # 计算节省百分比
            savings_percent = ((baseline_cost - cost_cny) / baseline_cost * 100) if baseline_cost > 0 else 0
            
            # 计算综合评分 (价格越低分越高，可靠性越高分越高)
            price_score = max(0, (baseline_cost - cost_cny) / baseline_cost * 100) if baseline_cost > 0 else 50
            reliability_score = model.reliability * 100
            speed_score = {"very_fast": 100, "fast": 80, "normal": 60}.get(model.speed, 50)
            
            total_score = price_score * 0.4 + reliability_score * 0.4 + speed_score * 0.2
            
            # 生成推荐理由
            reasons = []
            if "cost_effective" in model.strengths or model.input_price < 0.5:
                reasons.append("价格实惠")
            if model.reliability >= 0.98:
                reasons.append("稳定可靠")
            if model.speed in ["fast", "very_fast"]:
                reasons.append("响应快速")
            if task_type in ["document_processing"] and model.context_length > 1000000:
                reasons.append(f"支持超长上下文({model.context_length//10000}万token)")
            
            reason = "，".join(reasons) if reasons else "综合性能平衡"
            
            rec = Recommendation(
                model=model,
                estimated_input_cost=round(input_cost, 4),
                estimated_output_cost=round(output_cost, 4),
                total_cost_cny=round(cost_cny, 4),
                total_cost_usd=round(cost_usd, 4),
                savings_percent=round(savings_percent, 1),
                reason=reason,
                score=round(total_score, 2)
            )
            recommendations.append(rec)
        
        # 按评分排序
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations
    
    def compare_all(
        self, 
        input_tokens: int, 
        output_tokens: Optional[int] = None
    ) -> List[Dict]:
        """
        对比所有模型
        
        Args:
            input_tokens: 输入token数
            output_tokens: 输出token数
        
        Returns:
            所有模型成本对比
        """
        output_tokens = output_tokens or input_tokens // 2
        results = []
        
        for model_id, model in self.models.items():
            cost_cny, cost_usd = self.calculate_cost(model_id, input_tokens, output_tokens)
            results.append({
                "model_id": model_id,
                "model_name": model.name,
                "provider": model.provider,
                "cost_cny": round(cost_cny, 4),
                "cost_usd": round(cost_usd, 4),
                "currency": model.currency,
                "context_length": model.context_length,
                "speed": model.speed,
                "reliability": model.reliability
            })
        
        # 按价格排序
        results.sort(key=lambda x: x['cost_cny'])
        return results
    
    def analyze_budget(
        self,
        monthly_budget_cny: float,
        daily_calls: int = 100,
        avg_input_tokens: int = 1000,
        avg_output_tokens: Optional[int] = None
    ) -> Dict:
        """
        预算分析
        
        Args:
            monthly_budget_cny: 月度预算(人民币)
            daily_calls: 日均调用次数
            avg_input_tokens: 平均输入token数
            avg_output_tokens: 平均输出token数
        
        Returns:
            预算分析报告
        """
        avg_output_tokens = avg_output_tokens or avg_input_tokens // 2
        monthly_calls = daily_calls * 30
        
        analysis = {
            "budget_cny": monthly_budget_cny,
            "estimated_monthly_calls": monthly_calls,
            "model_options": []
        }
        
        for model_id, model in self.models.items():
            cost_per_call_cny, _ = self.calculate_cost(
                model_id, avg_input_tokens, avg_output_tokens
            )
            monthly_cost = cost_per_call_cny * monthly_calls
            
            # 计算能支持的调用次数
            affordable_calls = int(monthly_budget_cny / cost_per_call_cny) if cost_per_call_cny > 0 else 0
            
            status = "affordable" if monthly_cost <= monthly_budget_cny else "over_budget"
            
            analysis["model_options"].append({
                "model_id": model_id,
                "model_name": model.name,
                "cost_per_call_cny": round(cost_per_call_cny, 4),
                "monthly_cost_cny": round(monthly_cost, 2),
                "affordable_calls": affordable_calls,
                "status": status,
                "within_budget": monthly_cost <= monthly_budget_cny
            })
        
        # 按月度成本排序
        analysis["model_options"].sort(key=lambda x: x['monthly_cost_cny'])
        
        # 找出最佳性价比选项
        affordable = [m for m in analysis["model_options"] if m['within_budget']]
        if affordable:
            analysis["recommended"] = affordable[-1]  # 预算内最贵的(性能最好)
        else:
            analysis["recommended"] = analysis["model_options"][0]  # 最便宜的
        
        return analysis


# 便捷函数
def get_optimizer() -> TokenConsumerOptimizer:
    """获取优化器实例"""
    return TokenConsumerOptimizer()


def recommend_model(
    task_type: str,
    input_text: str,
    budget_level: str = "balanced"
) -> Dict:
    """
    快速推荐模型
    
    Args:
        task_type: 任务类型
        input_text: 输入文本 (自动估算token数)
        budget_level: 预算级别
    
    Returns:
        推荐结果
    """
    # 简单估算token数 (中文1字≈1token，英文1词≈1.3token)
    estimated_tokens = len(input_text)
    
    optimizer = get_optimizer()
    budget = BudgetLevel(budget_level) if budget_level in [e.value for e in BudgetLevel] else BudgetLevel.BALANCED
    
    recommendations = optimizer.recommend(
        task_type=task_type,
        input_tokens=estimated_tokens,
        budget_level=budget
    )
    
    if not recommendations:
        return {"error": "无法生成推荐"}
    
    top = recommendations[0]
    return {
        "recommended_model": top.model.name,
        "provider": top.model.provider,
        "estimated_cost_cny": top.total_cost_cny,
        "estimated_cost_usd": top.total_cost_usd,
        "reason": top.reason,
        "alternatives": [
            {
                "model": r.model.name,
                "cost_cny": r.total_cost_cny,
                "savings": f"{r.savings_percent}%"
            }
            for r in recommendations[1:3]
        ]
    }
