#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 수익 최적화 엔진
국가별 CPM, 광고 단가, 구매력을 기반으로 수익을 최대화하는 시스템
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class RevenueOptimizer:
    """수익 최적화 엔진"""
    
    def __init__(self):
        # 국가별 수익성 데이터 (실제 시장 데이터 기반)
        self.country_revenue_data = {
            "USA": {
                "cpm": 12.5,
                "ad_click_rate": 0.08,
                "affiliate_conversion": 0.035,
                "purchasing_power": 9.5,
                "market_size": 10.0,
                "competition": 8.5,
                "monthly_potential": 15000,
                "top_affiliate_categories": ["tech", "finance", "health", "insurance", "investment"],
                "ad_networks": ["Google AdSense", "Media.net", "Amazon Associates"],
                "premium_keywords": ["insurance", "mortgage", "credit card", "investment", "lawyer"]
            },
            "Germany": {
                "cpm": 8.7,
                "ad_click_rate": 0.06,
                "affiliate_conversion": 0.028,
                "purchasing_power": 8.9,
                "market_size": 8.5,
                "competition": 7.2,
                "monthly_potential": 10500,
                "top_affiliate_categories": ["automotive", "tech", "finance", "insurance"],
                "ad_networks": ["Google AdSense", "Zanox", "Amazon Associates"],
                "premium_keywords": ["versicherung", "kredit", "auto", "technologie", "investition"]
            },
            "UK": {
                "cpm": 9.1,
                "ad_click_rate": 0.075,
                "affiliate_conversion": 0.032,
                "purchasing_power": 8.7,
                "market_size": 7.8,
                "competition": 8.0,
                "monthly_potential": 9800,
                "top_affiliate_categories": ["finance", "property", "insurance", "tech"],
                "ad_networks": ["Google AdSense", "Amazon Associates", "Commission Junction"],
                "premium_keywords": ["mortgage", "insurance", "investment", "property", "credit"]
            },
            "Canada": {
                "cpm": 8.9,
                "ad_click_rate": 0.07,
                "affiliate_conversion": 0.03,
                "purchasing_power": 8.3,
                "market_size": 6.5,
                "competition": 6.8,
                "monthly_potential": 8200,
                "top_affiliate_categories": ["finance", "outdoor", "tech", "insurance"],
                "ad_networks": ["Google AdSense", "Amazon Associates", "ShareASale"],
                "premium_keywords": ["insurance", "mortgage", "investment", "outdoor", "winter"]
            },
            "Singapore": {
                "cpm": 8.3,
                "ad_click_rate": 0.065,
                "affiliate_conversion": 0.038,
                "purchasing_power": 8.8,
                "market_size": 5.2,
                "competition": 7.5,
                "monthly_potential": 7500,
                "top_affiliate_categories": ["luxury", "finance", "property", "tech"],
                "ad_networks": ["Google AdSense", "Amazon Associates", "Commission Factory"],
                "premium_keywords": ["property", "investment", "luxury", "finance", "premium"]
            },
            "Australia": {
                "cmp": 7.8,
                "ad_click_rate": 0.068,
                "affiliate_conversion": 0.029,
                "purchasing_power": 7.9,
                "market_size": 6.0,
                "competition": 6.2,
                "monthly_potential": 6800,
                "top_affiliate_categories": ["outdoor", "property", "finance", "tech"],
                "ad_networks": ["Google AdSense", "Amazon Associates", "Commission Factory"],
                "premium_keywords": ["property", "investment", "outdoor", "insurance", "finance"]
            },
            "Japan": {
                "cpm": 7.2,
                "ad_click_rate": 0.055,
                "affiliate_conversion": 0.025,
                "purchasing_power": 8.1,
                "market_size": 8.0,
                "competition": 9.0,
                "monthly_potential": 6200,
                "top_affiliate_categories": ["tech", "beauty", "fashion", "finance"],
                "ad_networks": ["Google AdSense", "Amazon Associates", "A8.net"],
                "premium_keywords": ["保険", "投資", "技術", "美容", "ファッション"]
            },
            "Korea": {
                "cpm": 6.2,
                "ad_click_rate": 0.045,
                "affiliate_conversion": 0.022,
                "purchasing_power": 7.2,
                "market_size": 6.8,
                "competition": 8.5,
                "monthly_potential": 4500,
                "top_affiliate_categories": ["beauty", "tech", "fashion", "food"],
                "ad_networks": ["Google AdSense", "Coupang Partners", "Amazon Associates"],
                "premium_keywords": ["보험", "투자", "뷰티", "기술", "패션"]
            }
        }
        
        # 수익성 순으로 정렬된 국가 목록
        self.top_countries = self._rank_countries_by_revenue()
        
    async def initialize_country_rankings(self):
        """국가별 수익성 순위 초기화"""
        logger.info("💰 국가별 수익성 순위 초기화 중...")
        self.top_countries = self._rank_countries_by_revenue()
        logger.info(f"🎯 수익성 Top 3: {self.top_countries[:3]}")
    
    def _rank_countries_by_revenue(self) -> List[str]:
        """수익성 기준으로 국가 순위 매기기"""
        country_scores = {}
        
        for country, data in self.country_revenue_data.items():
            # 종합 수익성 점수 계산
            revenue_score = (
                data.get("cpm", 0) * 0.3 +
                data.get("purchasing_power", 0) * 0.25 +
                data.get("market_size", 0) * 0.2 +
                (10 - data.get("competition", 5)) * 0.15 +  # 경쟁이 낮을수록 좋음
                data.get("ad_click_rate", 0) * 100 * 0.1
            )
            country_scores[country] = revenue_score
        
        # 점수 순으로 정렬
        return sorted(country_scores.keys(), key=lambda x: country_scores[x], reverse=True)
    
    def sort_countries_by_revenue(self, countries: List[str]) -> List[str]:
        """주어진 국가들을 수익성 순으로 정렬"""
        return [country for country in self.top_countries if country in countries]
    
    def get_country_revenue_potential(self, country: str) -> float:
        """국가별 월간 수익 잠재력 조회"""
        return self.country_revenue_data.get(country, {}).get("monthly_potential", 0)
    
    async def add_monetization(self, content: Dict[str, Any], country: str) -> Dict[str, Any]:
        """콘텐츠에 국가별 맞춤 수익화 요소 추가"""
        try:
            country_data = self.country_revenue_data.get(country, {})
            monetized_content = content.copy()
            
            # 기존 수익화 지점에 국가별 최적화 적용
            if "monetization_spots" in content:
                optimized_spots = []
                
                for spot in content["monetization_spots"]:
                    optimized_spot = await self._optimize_monetization_spot(spot, country_data)
                    optimized_spots.append(optimized_spot)
                
                monetized_content["monetization_spots"] = optimized_spots
            
            # 국가별 프리미엄 키워드 추가
            premium_keywords = country_data.get("premium_keywords", [])
            monetized_content["premium_keywords"] = premium_keywords
            
            # 추천 광고 네트워크
            monetized_content["recommended_ad_networks"] = country_data.get("ad_networks", [])
            
            # 수익 예측
            monetized_content["revenue_prediction"] = await self._calculate_revenue_prediction(
                content, country_data
            )
            
            logger.info(f"💰 {country} 수익화 최적화 완료")
            return monetized_content
            
        except Exception as e:
            logger.error(f"수익화 최적화 오류 ({country}): {e}")
            return content
    
    async def _optimize_monetization_spot(self, spot: Dict, country_data: Dict) -> Dict:
        """수익화 지점 최적화"""
        optimized_spot = spot.copy()
        
        # 국가별 CPM을 고려한 광고 타입 최적화
        cpm = country_data.get("cpm", 5.0)
        
        if spot["type"] == "display_ad":
            if cpm > 10:
                optimized_spot["ad_size"] = "premium_banner"
                optimized_spot["priority"] = "high"
            elif cpm > 7:
                optimized_spot["ad_size"] = "standard_banner"
                optimized_spot["priority"] = "medium"
            else:
                optimized_spot["ad_size"] = "text_ad"
                optimized_spot["priority"] = "low"
        
        elif spot["type"] == "affiliate_link":
            # 국가별 인기 카테고리 기반 제휴 추천
            top_categories = country_data.get("top_affiliate_categories", [])
            optimized_spot["recommended_categories"] = top_categories[:3]
            optimized_spot["conversion_rate"] = country_data.get("affiliate_conversion", 0.02)
        
        # 국가별 최적 배치 위치
        if cpm > 8:
            optimized_spot["placement"] = "above_fold"  # 높은 CPM 국가는 상단 배치
        else:
            optimized_spot["placement"] = "within_content"  # 낮은 CPM 국가는 콘텐츠 내 배치
        
        return optimized_spot
    
    async def _calculate_revenue_prediction(self, content: Dict, country_data: Dict) -> Dict:
        """수익 예측 계산"""
        try:
            # 기본 지표
            estimated_monthly_views = 10000  # 실제로는 키워드 분석 기반
            cpm = country_data.get("cpm", 5.0)
            click_rate = country_data.get("ad_click_rate", 0.05)
            conversion_rate = country_data.get("affiliate_conversion", 0.02)
            
            # 광고 수익 계산
            ad_revenue = (estimated_monthly_views * cpm) / 1000
            
            # 제휴 마케팅 수익 계산
            affiliate_clicks = estimated_monthly_views * click_rate
            affiliate_revenue = affiliate_clicks * conversion_rate * 50  # 평균 커미션 $50
            
            # 총 예상 수익
            total_revenue = ad_revenue + affiliate_revenue
            
            return {
                "monthly_ad_revenue": round(ad_revenue, 2),
                "monthly_affiliate_revenue": round(affiliate_revenue, 2),
                "total_monthly_revenue": round(total_revenue, 2),
                "estimated_views": estimated_monthly_views,
                "cpm": cpm,
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"수익 예측 계산 오류: {e}")
            return {"total_monthly_revenue": 0}
    
    def get_top_revenue_countries(self, limit: int = 5) -> List[Dict[str, Any]]:
        """수익성 상위 국가 목록 반환"""
        top_countries_data = []
        
        for country in self.top_countries[:limit]:
            data = self.country_revenue_data[country]
            top_countries_data.append({
                "country": country,
                "monthly_potential": data["monthly_potential"],
                "cpm": data["cpm"],
                "purchasing_power": data["purchasing_power"],
                "market_size": data["market_size"],
                "competition": data["competition"]
            })
        
        return top_countries_data
    
    async def optimize_keyword_strategy(self, keyword: str, target_countries: List[str]) -> Dict[str, Any]:
        """키워드별 국가 전략 최적화"""
        strategies = {}
        
        for country in target_countries:
            country_data = self.country_revenue_data.get(country, {})
            premium_keywords = country_data.get("premium_keywords", [])
            
            # 키워드가 프리미엄 키워드인지 확인
            is_premium = any(pk.lower() in keyword.lower() for pk in premium_keywords)
            
            strategies[country] = {
                "is_premium_keyword": is_premium,
                "recommended_content_type": "comparison" if is_premium else "guide",
                "monetization_level": "maximum" if is_premium else "high",
                "expected_competition": country_data.get("competition", 5),
                "revenue_multiplier": 1.5 if is_premium else 1.0,
                "recommended_ad_networks": country_data.get("ad_networks", [])[:2]
            }
        
        return strategies
    
    def get_revenue_insights(self) -> Dict[str, Any]:
        """수익 인사이트 및 추천사항"""
        total_potential = sum(
            data["monthly_potential"] for data in self.country_revenue_data.values()
        )
        
        return {
            "total_market_potential": total_potential,
            "top_revenue_country": self.top_countries[0],
            "recommended_focus_countries": self.top_countries[:3],
            "high_cpm_countries": [
                country for country, data in self.country_revenue_data.items()
                if data["cpm"] > 8.0
            ],
            "low_competition_countries": [
                country for country, data in self.country_revenue_data.items()
                if data["competition"] < 7.0
            ],
            "optimization_tips": [
                "미국, 독일, 영국에 집중하여 수익 최대화",
                "프리미엄 키워드 (보험, 투자, 부동산) 우선 타겟팅",
                "고CPM 국가에는 프리미엄 광고 배치",
                "저경쟁 국가에서 SEO 우위 확보"
            ]
        } 