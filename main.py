#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Gemini 기반 글로벌 블로그 완전자동화 시스템
최고 수익률을 위한 국가별 맞춤 자동화 플랫폼
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# 핵심 모듈 임포트
from core.gemini_engine import GeminiContentEngine
from core.revenue_optimizer import RevenueOptimizer
from core.trend_analyzer import GlobalTrendAnalyzer
from core.country_designer import CountryDesigner
from core.auto_publisher import AutoPublisher
from core.seo_optimizer import SEOOptimizer
from database.manager import DatabaseManager
from utils.scheduler import AutomationScheduler
from utils.analytics import RevenueTracker

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AutoBlogRequest(BaseModel):
    """블로그 자동 생성 요청 모델"""
    keywords: List[str] = Field(..., description="타겟 키워드 리스트")
    target_countries: List[str] = Field(
        default=["USA", "Germany", "UK", "Canada", "Singapore"],
        description="타겟 국가 (수익성 순)"
    )
    content_types: List[str] = Field(
        default=["review", "guide", "comparison", "news"],
        description="콘텐츠 타입"
    )
    monetization_level: str = Field(
        default="high",
        description="수익화 레벨 (low/medium/high/maximum)"
    )
    auto_publish: bool = Field(default=True, description="자동 배포 여부")
    seo_optimization: bool = Field(default=True, description="SEO 최적화 여부")

class SystemStatus(BaseModel):
    """시스템 상태 모델"""
    status: str
    active_blogs: int
    total_revenue: float
    top_performing_country: str
    automation_running: bool

# 전역 컴포넌트 초기화
gemini_engine = GeminiContentEngine()
revenue_optimizer = RevenueOptimizer()
trend_analyzer = GlobalTrendAnalyzer()
country_designer = CountryDesigner()
auto_publisher = AutoPublisher()
seo_optimizer = SEOOptimizer()
db_manager = DatabaseManager()
scheduler = AutomationScheduler()
revenue_tracker = RevenueTracker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 초기화
    logger.info("🚀 Gemini 블로그 자동화 시스템 시작!")
    await db_manager.initialize()
    await scheduler.start()
    
    # 수익성 높은 국가 우선 순위 설정
    await revenue_optimizer.initialize_country_rankings()
    
    # 초기 트렌드 분석 시작
    asyncio.create_task(trend_analyzer.start_continuous_monitoring())
    
    yield
    
    # 종료 시 정리
    await scheduler.stop()
    await db_manager.close()
    logger.info("시스템 정상 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="🌍 Gemini 글로벌 블로그 자동화 시스템",
    description="최고 수익률을 위한 AI 기반 글로벌 블로그 자동화 플랫폼",
    version="2.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """메인 대시보드"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Gemini 블로그 자동화 시스템</title>
        <meta charset="utf-8">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; backdrop-filter: blur(10px); }
            .controls { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            button { background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 5px; }
            button:hover { background: #45a049; }
            .country-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
            .country-card { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Gemini 글로벌 블로그 자동화 시스템</h1>
                <p>최고 수익률을 위한 AI 기반 글로벌 블로그 자동화 플랫폼</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>💰 예상 월 수익</h3>
                    <h2 id="revenue">$0</h2>
                </div>
                <div class="stat-card">
                    <h3>🌍 활성 국가</h3>
                    <h2 id="countries">0</h2>
                </div>
                <div class="stat-card">
                    <h3>📝 생성된 포스트</h3>
                    <h2 id="posts">0</h2>
                </div>
                <div class="stat-card">
                    <h3>⚡ 자동화 상태</h3>
                    <h2 id="status">준비중</h2>
                </div>
            </div>
            
            <div class="controls">
                <h3>🎯 수익 최적화 국가별 타겟</h3>
                <div class="country-grid">
                    <div class="country-card">🇺🇸 미국<br><strong>$15,000+/월</strong></div>
                    <div class="country-card">🇩🇪 독일<br><strong>$10,500+/월</strong></div>
                    <div class="country-card">🇬🇧 영국<br><strong>$9,800+/월</strong></div>
                    <div class="country-card">🇨🇦 캐나다<br><strong>$8,200+/월</strong></div>
                    <div class="country-card">🇸🇬 싱가포르<br><strong>$7,500+/월</strong></div>
                    <div class="country-card">🇦🇺 호주<br><strong>$6,800+/월</strong></div>
                    <div class="country-card">🇯🇵 일본<br><strong>$6,200+/월</strong></div>
                    <div class="country-card">🇰🇷 한국<br><strong>$4,500+/월</strong></div>
                </div>
                
                <div style="margin-top: 30px; text-align: center;">
                    <button onclick="startAutomation()">🚀 완전 자동화 시작</button>
                    <button onclick="generateContent()">📝 즉시 콘텐츠 생성</button>
                    <button onclick="viewAnalytics()">📊 수익 분석</button>
                    <button onclick="optimizeRevenue()">💎 수익 최적화</button>
                </div>
            </div>
        </div>
        
        <script>
            async function startAutomation() {
                const response = await fetch('/api/start-automation', { method: 'POST' });
                const data = await response.json();
                alert(data.message);
                updateStats();
            }
            
            async function generateContent() {
                const response = await fetch('/api/generate-content', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        keywords: ["AI", "technology", "investment", "health", "travel"],
                        target_countries: ["USA", "Germany", "UK", "Canada", "Singapore"],
                        monetization_level: "maximum"
                    })
                });
                const data = await response.json();
                alert(data.message);
            }
            
            async function updateStats() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    document.getElementById('revenue').textContent = '$' + data.total_revenue.toLocaleString();
                    document.getElementById('countries').textContent = data.active_countries;
                    document.getElementById('posts').textContent = data.total_posts;
                    document.getElementById('status').textContent = data.automation_running ? '자동 실행중' : '대기중';
                } catch (error) {
                    console.error('상태 업데이트 실패:', error);
                }
            }
            
            // 초기 로딩 및 주기적 업데이트
            updateStats();
            setInterval(updateStats, 10000);
        </script>
    </body>
    </html>
    """

@app.get("/api/status")
async def get_system_status() -> Dict[str, Any]:
    """시스템 현재 상태 조회"""
    try:
        status_data = await db_manager.get_system_status()
        revenue_data = await revenue_tracker.get_current_stats()
        
        return {
            "status": "active",
            "total_revenue": revenue_data.get("monthly_revenue", 0),
            "active_countries": len(revenue_optimizer.top_countries),
            "total_posts": status_data.get("total_posts", 0),
            "automation_running": scheduler.is_running(),
            "top_performing_country": revenue_data.get("top_country", "USA"),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"상태 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="상태 조회 실패")

@app.get("/api/trending-topics")
async def get_trending_topics():
    """실시간 글로벌 트렌딩 주제 조회"""
    try:
        trends = await trend_analyzer.get_revenue_optimized_trends()
        return {"status": "success", "trends": trends}
    except Exception as e:
        logger.error(f"트렌드 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="트렌드 조회 실패")

@app.post("/api/generate-content")
async def generate_content(request: AutoBlogRequest, background_tasks: BackgroundTasks):
    """Gemini AI 기반 국가별 맞춤 콘텐츠 생성"""
    try:
        # 백그라운드에서 콘텐츠 생성 시작
        background_tasks.add_task(
            process_global_content_generation,
            request.keywords,
            request.target_countries,
            request.content_types,
            request.monetization_level,
            request.auto_publish,
            request.seo_optimization
        )
        
        return {
            "status": "success",
            "message": f"🚀 {len(request.target_countries)}개국 대상 콘텐츠 생성이 시작되었습니다!",
            "estimated_revenue": sum([
                revenue_optimizer.get_country_revenue_potential(country) 
                for country in request.target_countries
            ]),
            "estimated_completion": "10-15분"
        }
    except Exception as e:
        logger.error(f"콘텐츠 생성 요청 오류: {e}")
        raise HTTPException(status_code=500, detail="콘텐츠 생성 요청 실패")

@app.post("/api/start-automation")
async def start_full_automation():
    """완전 자동화 모드 시작"""
    try:
        await scheduler.start_full_automation_mode()
        
        return {
            "status": "success",
            "message": "🔥 완전 자동화 모드가 시작되었습니다!",
            "features": [
                "실시간 트렌드 모니터링",
                "국가별 맞춤 콘텐츠 자동 생성",
                "수익 최적화 자동 조정",
                "글로벌 자동 배포",
                "24/7 수익 추적"
            ]
        }
    except Exception as e:
        logger.error(f"자동화 시작 오류: {e}")
        raise HTTPException(status_code=500, detail="자동화 시작 실패")

@app.get("/api/revenue-analytics")
async def get_revenue_analytics():
    """수익 분석 데이터"""
    try:
        analytics = await revenue_tracker.get_detailed_analytics()
        return {"status": "success", "analytics": analytics}
    except Exception as e:
        logger.error(f"수익 분석 오류: {e}")
        raise HTTPException(status_code=500, detail="수익 분석 실패")

async def process_global_content_generation(
    keywords: List[str],
    target_countries: List[str],
    content_types: List[str],
    monetization_level: str,
    auto_publish: bool,
    seo_optimization: bool
):
    """글로벌 콘텐츠 생성 프로세스"""
    try:
        logger.info(f"🌍 글로벌 콘텐츠 생성 시작: {len(keywords)}개 키워드 × {len(target_countries)}개국")
        
        # 수익성 순으로 국가 정렬
        sorted_countries = revenue_optimizer.sort_countries_by_revenue(target_countries)
        
        total_generated = 0
        for country in sorted_countries:
            logger.info(f"🎯 {country} 타겟 콘텐츠 생성 중...")
            
            # 국가별 디자인 테마 설정
            design_config = await country_designer.get_country_design(country)
            
            for keyword in keywords:
                for content_type in content_types:
                    try:
                        # 1. Gemini AI로 콘텐츠 생성
                        content = await gemini_engine.generate_content(
                            keyword=keyword,
                            country=country,
                            content_type=content_type,
                            monetization_level=monetization_level
                        )
                        
                        # 2. SEO 최적화
                        if seo_optimization:
                            content = await seo_optimizer.optimize_content(content, country)
                        
                        # 3. 수익화 요소 추가
                        content = await revenue_optimizer.add_monetization(content, country)
                        
                        # 4. 국가별 디자인 적용
                        styled_content = await country_designer.apply_design(content, design_config)
                        
                        # 5. 데이터베이스 저장
                        await db_manager.save_content(styled_content, country, keyword)
                        
                        # 6. 자동 배포
                        if auto_publish:
                            await auto_publisher.publish_to_vercel(styled_content, country)
                        
                        total_generated += 1
                        logger.info(f"✅ {country} - {keyword} ({content_type}) 생성 완료")
                        
                        # 과부하 방지를 위한 짧은 대기
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"❌ {country} - {keyword} 생성 실패: {e}")
                        continue
        
        logger.info(f"🎉 글로벌 콘텐츠 생성 완료! 총 {total_generated}개 생성")
        
        # 수익 추적 업데이트
        await revenue_tracker.update_content_metrics(total_generated, sorted_countries)
        
    except Exception as e:
        logger.error(f"글로벌 콘텐츠 생성 프로세스 오류: {e}")

if __name__ == "__main__":
    # 환경 변수 확인
    required_env_vars = ["GEMINI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"필수 환경 변수가 누락되었습니다: {missing_vars}")
        exit(1)
    
    logger.info("🚀 Gemini 글로벌 블로그 자동화 시스템 시작!")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    ) 