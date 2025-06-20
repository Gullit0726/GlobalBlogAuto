#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Gemini 글로벌 블로그 자동화 시스템 실행 스크립트
빠른 테스트 및 데모를 위한 스크립트
"""

import asyncio
import logging
import os
from datetime import datetime

# 환경 변수 설정 (테스트용)
os.environ["GEMINI_API_KEY"] = "test_key"
os.environ["PORT"] = "8000"

from core.gemini_engine import GeminiContentEngine
from core.revenue_optimizer import RevenueOptimizer
from core.country_designer import CountryDesigner
from core.auto_publisher import AutoPublisher

async def run_demo():
    """데모 실행"""
    print("🚀 Gemini 글로벌 블로그 자동화 시스템 데모 시작!\n")
    
    # 컴포넌트 초기화
    gemini_engine = GeminiContentEngine()
    revenue_optimizer = RevenueOptimizer()
    country_designer = CountryDesigner()
    auto_publisher = AutoPublisher()
    
    # 수익성 높은 국가 순위 초기화
    await revenue_optimizer.initialize_country_rankings()
    print(f"🎯 수익성 Top 3 국가: {revenue_optimizer.top_countries[:3]}\n")
    
    # 테스트 콘텐츠 생성
    test_keywords = ["AI investment", "cryptocurrency guide", "health insurance"]
    target_countries = ["USA", "Germany", "Japan"]
    
    for keyword in test_keywords:
        print(f"📝 '{keyword}' 키워드로 콘텐츠 생성 중...")
        
        for country in target_countries:
            try:
                # 1. Gemini AI 콘텐츠 생성
                content = await gemini_engine.generate_content(
                    keyword=keyword,
                    country=country,
                    content_type="guide",
                    monetization_level="high"
                )
                
                # 2. 수익화 최적화
                monetized_content = await revenue_optimizer.add_monetization(content, country)
                
                # 3. 국가별 디자인 적용
                design_config = await country_designer.get_country_design(country)
                styled_content = await country_designer.apply_design(monetized_content, design_config)
                
                # 4. Vercel 배포 (시뮬레이션)
                deployment_result = await auto_publisher.publish_to_vercel(styled_content, country)
                
                print(f"✅ {country} - {keyword}: {deployment_result.get('domain', 'N/A')}")
                
            except Exception as e:
                print(f"❌ {country} - {keyword}: 생성 실패 ({e})")
    
    print("\n🎉 데모 완료!")
    print("\n📊 수익 인사이트:")
    insights = revenue_optimizer.get_revenue_insights()
    for tip in insights["optimization_tips"]:
        print(f"💡 {tip}")
    
    print(f"\n💰 총 시장 잠재력: ${insights['total_market_potential']:,}/월")
    print(f"🎯 추천 집중 국가: {', '.join(insights['recommended_focus_countries'])}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🌍 Gemini 기반 글로벌 블로그 완전자동화 시스템")
    print("💰 최고 수익률을 위한 AI 기반 자동화 플랫폼")
    print("=" * 60)
    print()
    
    # 데모 실행
    asyncio.run(run_demo())
    
    print("\n" + "=" * 60)
    print("🚀 시스템을 실행하려면: python main.py")
    print("🌐 브라우저에서 접속: http://localhost:8000")
    print("📱 모바일에서도 완벽 지원!")
    print("=" * 60)

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    main() 