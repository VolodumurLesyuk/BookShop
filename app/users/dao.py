from app.dao.base import BaseDAO
from app.users.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def set_user_role(cls, user_id: int, role: str):
        valid_roles = [
            "is_user",
            "is_admin",
            "is_super_admin"
        ]
        if role not in valid_roles:
            raise ValueError(f"Недопустима роль: {role}")

        await cls.update(filter_by={"id": user_id}, **{r: False for r in valid_roles})

        await cls.update(filter_by={"id": user_id}, **{role: True})

        return await cls.find_one_or_none_by_id(user_id)
