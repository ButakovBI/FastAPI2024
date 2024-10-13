from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_root_page(request: Request):
    base_dir = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=base_dir / ".." / "templates")
    print(templates)
    return templates.TemplateResponse("root.html", {"request": request})
