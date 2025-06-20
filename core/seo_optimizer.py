#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 국가별 SEO 최적화 엔진
각 국가의 검색 알고리즘에 맞춘 SEO 자동 최적화
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """SEO 최적화 엔진"""
    
    def __init__(self):
        # 국가별 SEO 전략
        self.seo_strategies = {
            "USA": {
                "title_length": 60,
                "meta_description_length": 160,
                "keyword_density": 0.02,
                "heading_structure": "h1-h2-h3",
                "local_search_terms": ["America", "US", "United States"]
            },
            "Germany": {
                "title_length": 65,
                "meta_description_length": 165,
                "keyword_density": 0.025,
                "heading_structure": "h1-h2-h3-h4",
                "local_search_terms": ["Deutschland", "German", "Europa"]
            },
            "Japan": {
                "title_length": 30,  # 일본어는 더 짧게
                "meta_description_length": 120,
                "keyword_density": 0.015,
                "heading_structure": "h1-h2-h3",
                "local_search_terms": ["日本", "ジャパン", "和風"]
            }
        }
    
    async def optimize_content(self, content: Dict[str, Any], country: str) -> Dict[str, Any]:
        """국가별 SEO 최적화"""
        try:
            strategy = self.seo_strategies.get(country, self.seo_strategies["USA"])
            optimized_content = content.copy()
            
            # 제목 최적화
            optimized_content["title"] = self._optimize_title(
                content.get("title", ""), strategy
            )
            
            # 메타 설명 최적화
            optimized_content["meta_description"] = self._optimize_meta_description(
                content.get("meta_description", ""), strategy
            )
            
            # 키워드 최적화
            optimized_content["optimized_keywords"] = self._optimize_keywords(
                content, strategy
            )
            
            # 구조화 데이터 추가
            optimized_content["schema_markup"] = self._generate_schema_markup(
                optimized_content, country
            )
            
            logger.info(f"🔍 {country} SEO 최적화 완료")
            return optimized_content
            
        except Exception as e:
            logger.error(f"SEO 최적화 오류 ({country}): {e}")
            return content
    
    def _optimize_title(self, title: str, strategy: Dict) -> str:
        """제목 최적화"""
        max_length = strategy["title_length"]
        
        if len(title) > max_length:
            return title[:max_length-3] + "..."
        
        return title
    
    def _optimize_meta_description(self, description: str, strategy: Dict) -> str:
        """메타 설명 최적화"""
        max_length = strategy["meta_description_length"]
        
        if len(description) > max_length:
            return description[:max_length-3] + "..."
        
        return description
    
    def _optimize_keywords(self, content: Dict, strategy: Dict) -> List[str]:
        """키워드 최적화"""
        primary_keyword = content.get("metadata", {}).get("keyword", "")
        local_terms = strategy["local_search_terms"]
        
        optimized_keywords = [primary_keyword] + local_terms[:2]
        return optimized_keywords
    
    def _generate_schema_markup(self, content: Dict, country: str) -> Dict:
        """구조화 데이터 생성"""
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": content.get("title", ""),
            "description": content.get("meta_description", ""),
            "author": {
                "@type": "Organization",
                "name": f"Global Blog {country}"
            },
            "datePublished": datetime.now().isoformat(),
            "inLanguage": "en" if country in ["USA", "UK", "Australia"] else "auto"
        } 