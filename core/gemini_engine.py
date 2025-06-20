#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Gemini AI 콘텐츠 생성 엔진
국가별 문화와 수익성을 고려한 최적화된 콘텐츠 자동 생성
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import random

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logging.warning("google-generativeai 패키지가 설치되지 않았습니다. 시뮬레이션 모드로 실행됩니다.")

logger = logging.getLogger(__name__)

class GeminiContentEngine:
    """Gemini Pro 기반 국가별 맞춤 콘텐츠 생성 엔진"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        # 국가별 문화 특성 및 수익 최적화 데이터
        self.country_profiles = {
            "USA": {
                "language": "en-US",
                "cultural_tone": "confident, direct, benefit-focused",
                "writing_style": "scannable, action-oriented, data-driven",
                "high_value_keywords": ["best", "top", "review", "guide", "money", "investment", "insurance", "credit"],
                "avoid_topics": ["politics", "religion"],
                "preferred_structure": "headline -> benefits -> proof -> CTA",
                "cpm_multiplier": 12.5,
                "currency": "USD",
                "avg_word_count": 1500,
                "engagement_triggers": ["limited time", "exclusive", "proven", "guaranteed"],
                "local_references": ["American", "US", "States", "dollar"]
            },
            "Germany": {
                "language": "de-DE", 
                "cultural_tone": "thorough, technical, quality-focused",
                "writing_style": "detailed, structured, evidence-based",
                "high_value_keywords": ["qualität", "test", "vergleich", "bewertung", "technologie", "auto", "investition"],
                "avoid_topics": ["aggressive sales"],
                "preferred_structure": "introduction -> detailed analysis -> technical specs -> conclusion",
                "cmp_multiplier": 8.7,
                "currency": "EUR",
                "avg_word_count": 2000,
                "engagement_triggers": ["qualität", "präzision", "effizienz", "innovation"],
                "local_references": ["Deutschland", "deutsch", "europäisch", "Euro"]
            },
            "Japan": {
                "language": "ja-JP",
                "cultural_tone": "polite, respectful, detail-oriented",
                "writing_style": "structured, visual, trend-conscious",
                "high_value_keywords": ["レビュー", "比較", "おすすめ", "ランキング", "技術", "投資", "保険"],
                "avoid_topics": ["confrontational content"],
                "preferred_structure": "greeting -> detailed explanation -> comparison -> recommendation",
                "cpm_multiplier": 7.2,
                "currency": "JPY",
                "avg_word_count": 1200,
                "engagement_triggers": ["最新", "人気", "おすすめ", "限定"],
                "local_references": ["日本", "日本人", "和風", "円"]
            },
            "UK": {
                "language": "en-GB",
                "cultural_tone": "witty, professional, balanced",
                "writing_style": "sophisticated, conversational, informative",
                "high_value_keywords": ["brilliant", "proper", "guide", "review", "investment", "insurance", "property"],
                "avoid_topics": ["overly aggressive sales"],
                "preferred_structure": "engaging intro -> balanced analysis -> pros/cons -> conclusion",
                "cpm_multiplier": 9.1,
                "currency": "GBP",
                "avg_word_count": 1400,
                "engagement_triggers": ["exclusive", "brilliant", "proper", "essential"],
                "local_references": ["British", "UK", "Britain", "pound"]
            },
            "Canada": {
                "language": "en-CA",
                "cultural_tone": "friendly, inclusive, practical",
                "writing_style": "warm, helpful, community-focused",
                "high_value_keywords": ["best", "guide", "review", "canadian", "winter", "investment", "insurance"],
                "avoid_topics": ["divisive content"],
                "preferred_structure": "friendly intro -> practical advice -> community perspective -> helpful conclusion",
                "cpm_multiplier": 8.9,
                "currency": "CAD",
                "avg_word_count": 1300,
                "engagement_triggers": ["community", "helpful", "practical", "reliable"],
                "local_references": ["Canadian", "Canada", "maple", "dollar"]
            },
            "Singapore": {
                "language": "en-SG",
                "cultural_tone": "multicultural, premium-focused, efficient",
                "writing_style": "concise, international, luxury-oriented",
                "high_value_keywords": ["premium", "luxury", "efficient", "smart", "investment", "property", "finance"],
                "avoid_topics": ["cultural insensitivity"],
                "preferred_structure": "executive summary -> key benefits -> premium features -> action steps",
                "cpm_multiplier": 8.3,
                "currency": "SGD",
                "avg_word_count": 1200,
                "engagement_triggers": ["premium", "exclusive", "smart", "efficient"],
                "local_references": ["Singapore", "Singaporean", "SG", "dollar"]
            },
            "Australia": {
                "language": "en-AU",
                "cultural_tone": "casual, friendly, outdoor-focused",
                "writing_style": "relaxed, authentic, practical",
                "high_value_keywords": ["mate", "best", "review", "aussie", "outdoor", "investment", "property"],
                "avoid_topics": ["overly formal content"],
                "preferred_structure": "casual intro -> straight-talking advice -> real examples -> practical conclusion",
                "cpm_multiplier": 7.8,
                "currency": "AUD",
                "avg_word_count": 1100,
                "engagement_triggers": ["authentic", "practical", "reliable", "fair dinkum"],
                "local_references": ["Australian", "Aussie", "mate", "dollar"]
            },
            "Korea": {
                "language": "ko-KR",
                "cultural_tone": "trend-focused, community-oriented, respectful",
                "writing_style": "visual, trendy, social-proof driven",
                "high_value_keywords": ["리뷰", "추천", "가성비", "인기", "트렌드", "투자", "보험"],
                "avoid_topics": ["controversial topics"],
                "preferred_structure": "트렌드 소개 -> 상세 분석 -> 커뮤니티 의견 -> 추천",
                "cpm_multiplier": 6.2,
                "currency": "KRW",
                "avg_word_count": 1000,
                "engagement_triggers": ["인기", "트렌드", "추천", "가성비"],
                "local_references": ["한국", "한국인", "국내", "원"]
            }
        }
        
        # Gemini 모델 초기화
        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini Pro 모델 초기화 완료")
        else:
            logger.warning("⚠️ Gemini API 키가 없거나 패키지가 없습니다. 시뮬레이션 모드로 실행됩니다.")
    
    async def generate_content(
        self,
        keyword: str,
        country: str,
        content_type: str = "guide",
        monetization_level: str = "high"
    ) -> Dict[str, Any]:
        """국가별 맞춤 콘텐츠 생성"""
        try:
            logger.info(f"🎯 {country} 대상 '{keyword}' 콘텐츠 생성 시작")
            
            # 국가 프로필 가져오기
            profile = self.country_profiles.get(country, self.country_profiles["USA"])
            
            # 프롬프트 생성
            prompt = self._create_optimized_prompt(keyword, country, content_type, monetization_level, profile)
            
            # Gemini로 콘텐츠 생성
            if self.model:
                content = await self._generate_with_gemini(prompt, profile)
            else:
                content = self._generate_simulation_content(keyword, country, profile)
            
            # 메타데이터 추가
            content["metadata"] = {
                "keyword": keyword,
                "country": country,
                "content_type": content_type,
                "monetization_level": monetization_level,
                "generated_at": datetime.now().isoformat(),
                "language": profile["language"],
                "estimated_revenue": self._calculate_revenue_potential(keyword, country, profile),
                "word_count": len(content["content"].split()) if "content" in content else 0
            }
            
            logger.info(f"✅ {country} - {keyword} 콘텐츠 생성 완료")
            return content
            
        except Exception as e:
            logger.error(f"❌ {country} - {keyword} 콘텐츠 생성 실패: {e}")
            return self._generate_fallback_content(keyword, country)
    
    def _create_optimized_prompt(
        self,
        keyword: str,
        country: str,
        content_type: str,
        monetization_level: str,
        profile: Dict
    ) -> str:
        """수익 최적화된 프롬프트 생성"""
        
        monetization_instructions = {
            "low": "Include 1-2 subtle product recommendations",
            "medium": "Include 3-4 strategic affiliate opportunities and 2 ad placements",
            "high": "Include 5-6 monetization opportunities with natural product integration",
            "maximum": "Maximize revenue with 8+ monetization points while maintaining quality"
        }
        
        content_type_templates = {
            "guide": f"comprehensive guide about {keyword}",
            "review": f"detailed review and analysis of {keyword}",
            "comparison": f"comparison article about different {keyword} options",
            "news": f"latest news and trends about {keyword}",
            "tutorial": f"step-by-step tutorial for {keyword}"
        }
        
        prompt = f"""
Create a high-quality, engaging {content_type_templates.get(content_type, 'article')} specifically for {country} audience.

CONTENT REQUIREMENTS:
- Primary keyword: "{keyword}"
- Target country: {country}
- Language: {profile['language']}
- Cultural tone: {profile['cultural_tone']}
- Writing style: {profile['writing_style']}
- Word count: approximately {profile['avg_word_count']} words
- Structure: {profile['preferred_structure']}

CULTURAL ADAPTATION:
- Use cultural references: {', '.join(profile['local_references'])}
- Include engagement triggers: {', '.join(profile['engagement_triggers'])}
- Avoid: {', '.join(profile.get('avoid_topics', []))}
- Currency references: {profile['currency']}

HIGH-VALUE OPTIMIZATION:
- Incorporate these high-value keywords naturally: {', '.join(profile['high_value_keywords'][:5])}
- {monetization_instructions[monetization_level]}
- Include clear calls-to-action
- Add trust signals and social proof
- Optimize for search intent

CONTENT STRUCTURE:
1. Compelling headline with emotional hook
2. Introduction that addresses user pain points
3. Main content with clear subheadings
4. Practical examples and case studies
5. Comparison sections where relevant
6. Strong conclusion with clear next steps
7. SEO-optimized meta description

Make the content authentic, valuable, and culturally appropriate for {country} readers while maximizing revenue potential.
"""
        
        return prompt
    
    async def _generate_with_gemini(self, prompt: str, profile: Dict) -> Dict[str, Any]:
        """Gemini Pro로 실제 콘텐츠 생성"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            content_text = response.text
            
            # 콘텐츠 파싱 및 구조화
            parsed_content = self._parse_generated_content(content_text, profile)
            
            return parsed_content
            
        except Exception as e:
            logger.error(f"Gemini 생성 오류: {e}")
            raise
    
    def _generate_simulation_content(self, keyword: str, country: str, profile: Dict) -> Dict[str, Any]:
        """시뮬레이션 콘텐츠 생성 (API 없을 때)"""
        
        sample_titles = [
            f"Ultimate {keyword.title()} Guide for {country} Readers",
            f"Best {keyword.title()} Options in {country} - Expert Review",
            f"Complete {keyword.title()} Analysis: {country} Edition",
            f"Top {keyword.title()} Recommendations for {profile['currency']} Budget"
        ]
        
        sample_content = f"""
# {random.choice(sample_titles)}

## Introduction
Welcome to our comprehensive guide about {keyword}, specifically tailored for {country} readers. Understanding {keyword} is crucial in today's market, especially when considering {profile['currency']} investments.

## Why {keyword.title()} Matters in {country}
{keyword.title()} has become increasingly important for {', '.join(profile['local_references'])} consumers. Here's what you need to know:

### Key Benefits
- Enhanced value for your {profile['currency']}
- {profile['engagement_triggers'][0].title()} solutions
- Proven results in {country} market
- Expert-recommended approaches

## Detailed Analysis
Our team has analyzed {keyword} from multiple perspectives relevant to {country} users:

### Performance Metrics
- Reliability: 95%
- User satisfaction: 4.8/5 stars
- Value for {profile['currency']}: Excellent
- {country} market penetration: High

### Top Recommendations
1. **Premium Option**: Best for high-budget users
2. **Value Choice**: Perfect {profile['currency']} balance
3. **Budget-Friendly**: Great for beginners
4. **{country} Exclusive**: Local market leader

## Expert Comparison
When compared to alternatives in the {country} market, {keyword} stands out for:
- Superior quality standards
- Competitive {profile['currency']} pricing
- Excellent local support
- {profile['engagement_triggers'][1].title()} performance

## Conclusion
After thorough analysis, we recommend {keyword} for {country} users. The combination of features, reliability, and {profile['currency']} value makes it an excellent choice.

### Next Steps
Ready to get started? Here are your options:
- Compare providers in {country}
- Read user reviews from {profile['local_references'][0]} customers  
- Take advantage of current {profile['currency']} offers
- Contact local experts for personalized advice
        """
        
        return {
            "title": random.choice(sample_titles),
            "content": sample_content.strip(),
            "meta_description": f"Comprehensive {keyword} guide for {country}. Expert insights, comparisons, and {profile['currency']} recommendations.",
            "tags": [keyword, country.lower(), "guide", "review", "expert"],
            "monetization_spots": self._identify_monetization_opportunities(sample_content),
            "seo_score": random.randint(75, 95)
        }
    
    def _parse_generated_content(self, content_text: str, profile: Dict) -> Dict[str, Any]:
        """생성된 콘텐츠 파싱 및 구조화"""
        lines = content_text.split('\n')
        
        title = lines[0].replace('#', '').strip() if lines else "Generated Content"
        
        # 메타 설명 추출 (마지막 문단에서)
        meta_description = ""
        if len(lines) > 10:
            last_paragraph = ' '.join(lines[-3:]).replace('#', '').strip()
            if len(last_paragraph) > 50:
                meta_description = last_paragraph[:155] + "..."
        
        return {
            "title": title,
            "content": content_text,
            "meta_description": meta_description or f"Expert guide about {title.lower()}",
            "tags": self._extract_tags(content_text),
            "monetization_spots": self._identify_monetization_opportunities(content_text),
            "seo_score": self._calculate_seo_score(content_text, profile)
        }
    
    def _identify_monetization_opportunities(self, content: str) -> List[Dict]:
        """수익화 기회 식별"""
        opportunities = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # 제품 언급 감지
            if any(word in line.lower() for word in ['product', 'tool', 'service', 'option', 'solution']):
                opportunities.append({
                    "type": "affiliate_link",
                    "position": i,
                    "context": "product_mention",
                    "revenue_potential": "high"
                })
            
            # 섹션 구분 감지 (광고 삽입 지점)
            if line.startswith('##') and i > 0:
                opportunities.append({
                    "type": "display_ad",
                    "position": i,
                    "context": "section_break",
                    "revenue_potential": "medium"
                })
            
            # 비교 섹션 감지
            if any(word in line.lower() for word in ['vs', 'compare', 'comparison', 'alternative']):
                opportunities.append({
                    "type": "comparison_table",
                    "position": i,
                    "context": "comparison_section",
                    "revenue_potential": "very_high"
                })
        
        return opportunities
    
    def _calculate_revenue_potential(self, keyword: str, country: str, profile: Dict) -> float:
        """수익 잠재력 계산"""
        base_cpm = profile.get("cpm_multiplier", 5.0)
        
        # 키워드 가치 승수
        keyword_multiplier = 1.0
        high_value_keywords = profile.get("high_value_keywords", [])
        
        for hvk in high_value_keywords:
            if hvk.lower() in keyword.lower():
                keyword_multiplier += 0.3
        
        # 예상 페이지뷰 (키워드 인기도 기반)
        estimated_pageviews = 1000  # 기본값, 실제로는 키워드 분석 도구 사용
        
        # 수익 계산
        monthly_revenue = (base_cpm * estimated_pageviews * keyword_multiplier) / 1000
        
        return round(monthly_revenue, 2)
    
    def _extract_tags(self, content: str) -> List[str]:
        """콘텐츠에서 태그 추출"""
        # 간단한 태그 추출 로직
        words = content.lower().split()
        common_tags = ["guide", "review", "tips", "best", "top", "how", "tutorial", "analysis"]
        
        extracted_tags = []
        for tag in common_tags:
            if tag in words:
                extracted_tags.append(tag)
        
        return extracted_tags[:10]  # 최대 10개
    
    def _calculate_seo_score(self, content: str, profile: Dict) -> int:
        """SEO 점수 계산"""
        score = 50  # 기본 점수
        
        # 글자 수 체크
        word_count = len(content.split())
        target_count = profile.get("avg_word_count", 1000)
        
        if abs(word_count - target_count) <= 200:
            score += 15
        
        # 제목 구조 체크
        if content.count('#') >= 3:
            score += 10
        
        # 고가치 키워드 포함 체크
        high_value_keywords = profile.get("high_value_keywords", [])
        for keyword in high_value_keywords[:3]:
            if keyword.lower() in content.lower():
                score += 5
        
        return min(score, 100)
    
    def _generate_fallback_content(self, keyword: str, country: str) -> Dict[str, Any]:
        """대안 콘텐츠 (오류 시)"""
        return {
            "title": f"Guide to {keyword.title()} in {country}",
            "content": f"This is a comprehensive guide about {keyword} for {country} readers. Content generation is in progress.",
            "meta_description": f"Learn about {keyword} with our expert guide for {country}.",
            "tags": [keyword, country.lower(), "guide"],
            "monetization_spots": [],
            "seo_score": 60,
            "metadata": {
                "keyword": keyword,
                "country": country,
                "generated_at": datetime.now().isoformat(),
                "status": "fallback"
            }
        } 