from dataclasses import fields
from fastapi import FastAPI, HTTPException
from tortoise import models, field
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel 
from typing import List

# 1. FastAPI 애플리케이션 인스턴스 생성
class Diary(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    date = fields.DateField()
    mood = fields.CharField(max_length=50)

    def __str__(self):
        return self.title
    
# 3. Pydantic 스키마 정의 (데이터 유효성 검사 및 응답 형식 지정)
class DiaryOut_Pydantic(BaseModel):
    user_id: int
    title: str
    content: str
    date: str
    mood: str

# 응답 스키마 (데이터베이스 모델과 동일한 구조)
class DiaryOut_Pydantic(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date: str
    mood: str

# 4. API 엔드포인트 구현 (비동기 함수 async/await 사용)

@app.get("/api/diaries", response_model=List[DiaryOut_Pydantic])
async def get_diaries():
    """모든 일기 목록을 조회합니다"""
    # .all()은 비동기 작업이므로 await 사용
    return await DiaryOut_Pydantic.from_queryset(Diary.all())

@app.get("/api/diaries/{diary_id}", response_model=DiaryOut_Pydantic)
async def get_diary(diary_id:int):
    """특정 ID의 일기 항목을 상세 조회합니다."""
    diary = await Diary.get_or_none(id=diary_id)
    if diary is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return await DiaryOut_Pydantic.from_tortoise_object(diary)

@app.post("/api/diaries", response_model=DiaryOut_Pydantic, status_code=201)
async def create_diary(diary_in: DiaryOut_Pydantic):
    """새로운 일기 항목을 생성합니다."""
    # .create()은 비동기 작업이므로 await 사용
    diary = await Diary.create(**diary_in.model_dump())
    return await DiaryOut_Pydantic.from_tortoise_object(diary)

@app.put("/api/diaries/{diary_id}", response_model=DiaryOut_Pydantic)
async def update_diary(diary_id: int, diary_in: DiaryOut_Pydantic):
    """특정 ID의 일기 항목을 수정합니다."""
    await Diary.filter(id=diary_id).update(**diary_in.model_dump())
    return await get_diary(diary_id) # 업데이트된 객체 반환

@app.delete("/api/diaries/{diary_id}", status_code=204)
async def delete_diary(diary_id: int):
    """특정 ID의 일기 항목을 삭제합니다."""
    delete_count = await Diary.filter(id=diary_id).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return {"message: Deleted"}

# 5. Tortoise ORM을 FastAPI 앱에 등록 및 초기화
register_tortoise(
    app,
    db_url="sqlite://./diary.sqlite3", #SQLite DB 파일 경로 설정
    modules={"models": ["main"]}, # 모델이 정의된 모듈 지정
    generate_shemas=True, # 앱 시작 시 DB 스키마 자동 생성
    add_exeption_handlers=True,
)

# 6. 애플리케이션 실행 (uvicorn 사용 권장)
# uvicorn main:app --reload 명령어로 실행 가능
# 위 주석은 실행 방법 안내용으로, 실제 코드에는 포함되지 않습니다.