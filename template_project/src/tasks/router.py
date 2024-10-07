from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_config import current_user
from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
async def get_dashboard_report(
    background_tasks: BackgroundTasks, user=Depends(current_user)
):
    # 1400 ms - ожидание
    send_email_report_dashboard(user.username)
    # 500 ms - на фоне FastAPI в event loop'е или в другом треде
    background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - выполнение воркером Celery в отдельном процессе
    send_email_report_dashboard.delay(user.username)
    return {"status": 200, "data": "Письмо отправлено", "details": None}
