from fastapi import APIRouter,HTTPException
import os
appname = os.environ.get('appname')


router = APIRouter(
     prefix="",
    tags=["basic_endpoints"]
)

@router.get("/raise-error")
async def raise_error(should_fail: bool):
    if should_fail:
        raise HTTPException(status_code=400, detail="This is a bad request")
    return {"message": "Success"}

@router.get("/")
def welcome():
    return f"welcome to {appname}"

@router.get("/health")
def health():
    return f"App {appname} doing fine ..."
