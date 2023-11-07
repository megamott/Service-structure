from app.models.common import User


class UserRepository:
    async def all(self):
        return await User.query.order_by(User.id.desc()).gino.all()