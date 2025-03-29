from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from jose import JWTError, jwt

from app.config import get_auth_data
from app.users.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User
from app.users.schemas import SUserRegister, SUserAuth, SUserRole

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Користувач вже існує'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Реєстрація пройшла успішно!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Невірна пошта або пароль')

    user_data = {"sub": str(check.id)}

    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    response.set_cookie(key="users_refresh_token", value=refresh_token, httponly=True, max_age=2592000)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response):
    refresh_token = request.cookies.get('users_refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token не знайдено")

    try:
        auth_data = get_auth_data()
        payload = jwt.decode(refresh_token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token невалідний")

    expire = payload.get("exp")
    if not expire or datetime.fromtimestamp(expire, tz=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token прострочений")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Користувач не визначений")

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Користувач не знайдений")

    # Створення нових токенів
    user_data = {"sub": str(user.id)}
    new_access_token = create_access_token(user_data)
    new_refresh_token = create_refresh_token(user_data)

    response.set_cookie(key="users_access_token", value=new_access_token, httponly=True, max_age=900)
    response.set_cookie(key="users_refresh_token", value=new_refresh_token, httponly=True, max_age=2592000)
    return {"message": "Токени оновлено"}



@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("users_access_token")
    response.delete_cookie("users_refresh_token")
    return {"message": "Вихід виконано"}


@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()



@router.post("/give_role/{user_id}/{role}", response_model=SUserRole)
async def give_role(user_data: User = Depends(get_current_admin_user), user_id: int = 2, role: str = "is_user"):
    try:
        user = await UsersDAO.set_user_role(user_id, role)
        if not user:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))