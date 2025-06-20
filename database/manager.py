#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ 데이터베이스 관리자
콘텐츠 및 수익 데이터 관리
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import sqlite3
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """데이터베이스 관리자"""
    
    def __init__(self):
        self.db_path = "global_blog.db"
        self.connection = None
    
    async def initialize(self):
        """데이터베이스 초기화"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            await self._create_tables()
            logger.info("🗄️ 데이터베이스 초기화 완료")
        except Exception as e:
            logger.error(f"데이터베이스 초기화 오류: {e}")
    
    async def _create_tables(self):
        """테이블 생성"""
        cursor = self.connection.cursor()
        
        # 콘텐츠 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                country TEXT NOT NULL,
                keyword TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                revenue_potential REAL DEFAULT 0
            )
        """)
        
        # 수익 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                monthly_revenue REAL DEFAULT 0,
                content_count INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
    
    async def save_content(self, content: Dict[str, Any], country: str, keyword: str):
        """콘텐츠 저장"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO content (title, content, country, keyword, revenue_potential)
                VALUES (?, ?, ?, ?, ?)
            """, (
                content.get("title", ""),
                content.get("content", ""),
                country,
                keyword,
                content.get("metadata", {}).get("estimated_revenue", 0)
            ))
            self.connection.commit()
            logger.info(f"💾 {country} - {keyword} 콘텐츠 저장 완료")
        except Exception as e:
            logger.error(f"콘텐츠 저장 오류: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        try:
            cursor = self.connection.cursor()
            
            # 총 포스트 수
            cursor.execute("SELECT COUNT(*) FROM content")
            total_posts = cursor.fetchone()[0]
            
            # 국가별 포스트 수
            cursor.execute("SELECT country, COUNT(*) FROM content GROUP BY country")
            country_stats = dict(cursor.fetchall())
            
            return {
                "total_posts": total_posts,
                "country_stats": country_stats,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"상태 조회 오류: {e}")
            return {"total_posts": 0, "country_stats": {}}
    
    async def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            logger.info("데이터베이스 연결 종료") 