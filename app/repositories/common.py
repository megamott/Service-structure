from app.models.users import User


class UserRepository:
    async def list(self):
        return await User.query.order_by(User.id.desc()).gino.all()