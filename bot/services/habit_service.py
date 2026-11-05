from datetime import date
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Habit, HabitLog
from core.exceptions import (
    HabitNotFoundError,
    HabitAlreadyCompletedTodayError,
    EmptyHabitTitleError
)


class HabitService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: Optional[str], first_name: str) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def create_habit(self, telegram_id: int, title: str) -> Habit:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise EmptyHabitTitleError("Назва звички не може бути порожньою.")

        user = await self.get_or_create_user(telegram_id, None, "Користувач")
        habit = Habit(user_id=user.id, title=cleaned_title)
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit

    async def get_user_habits(self, telegram_id: int) -> List[Habit]:
        stmt = (
            select(Habit)
            .join(User)
            .where(User.telegram_id == telegram_id)
            .order_by(Habit.id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def mark_habit_completed(self, habit_id: int, telegram_id: int) -> HabitLog:
        stmt = (
            select(Habit)
            .join(User)
            .where(Habit.id == habit_id, User.telegram_id == telegram_id)
        )
        result = await self.session.execute(stmt)
        habit = result.scalar_one_or_none()

        if not habit:
            raise HabitNotFoundError(habit_id)

        today = date.today()
        check_stmt = select(HabitLog).where(
            HabitLog.habit_id == habit.id,
            HabitLog.completed_date == today
        )
        check_res = await self.session.execute(check_stmt)
        if check_res.scalar_one_or_none():
            raise HabitAlreadyCompletedTodayError(habit.title)

        log = HabitLog(habit_id=habit.id, completed_date=today)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log
