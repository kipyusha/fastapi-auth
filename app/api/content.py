from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user, require_level_1, require_level_2, require_level_3
from app.models.user import User

router = APIRouter(prefix="/content")

LESSONS = {
    1: {
        "id": 1,
        "title": "Основы Python",
        "text": "Python - это высокоуровневый язык программирования...",
        "video_url": "https://example.com/video/python-basics",
        "trainer_url": "https://example.com/trainer/python-quiz"
    },
    2: {
        "id": 2,
        "title": "Работа с FastAPI",
        "text": "FastAPI - это современный веб-фреймворк для Python...",
        "video_url": "https://example.com/video/fastapi-tutorial",
        "trainer_url": "https://example.com/trainer/fastapi-quiz"
    }
}

@router.get("/lessons/{lesson_id}/text")
async def get_lesson_text(
    lesson_id: int,
    current_user: User = Depends(require_level_1),
    db: AsyncSession = Depends(get_db)
):
    if lesson_id not in LESSONS:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson = LESSONS[lesson_id]
    return {
        "id": lesson["id"],
        "title": lesson["title"],
        "text": lesson["text"],
        "access_level_required": 1
    }

@router.get("/lessons/{lesson_id}/video")
async def get_lesson_video(
    lesson_id: int,
    current_user: User = Depends(require_level_2),
    db: AsyncSession = Depends(get_db)
):

    if lesson_id not in LESSONS:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    if not current_user.has_access_video():
        raise HTTPException(status_code=403, detail="Video access requires level 2 subscription")
    
    lesson = LESSONS[lesson_id]
    return {
        "id": lesson["id"],
        "title": lesson["title"],
        "video_url": lesson["video_url"],
        "access_level_required": 2
    }

@router.get("/lessons/{lesson_id}/trainer")
async def get_lesson_trainer(
    lesson_id: int,
    current_user: User = Depends(require_level_3),
    db: AsyncSession = Depends(get_db)
):

    if lesson_id not in LESSONS:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    if not current_user.has_access_trainer():
        raise HTTPException(status_code=403, detail="Trainer access requires level 3 subscription")
    
    lesson = LESSONS[lesson_id]
    return {
        "id": lesson["id"],
        "title": lesson["title"],
        "trainer_url": lesson["trainer_url"],
        "access_level_required": 3
    }

@router.get("/my-access")
async def get_my_access_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    from app.services.subscription_service import check_user_access
    return await check_user_access(current_user.id, db)