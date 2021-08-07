from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends


from db.repository.jobs_data_access_layer import JobBoard
from depends import get_job_db


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home_page(request: Request, list_jobs: JobBoard = Depends(get_job_db)):
    jobs = await list_jobs.get_all_jobs()
    return templates.TemplateResponse("jobs/homepage.html", {"request": request, "jobs": jobs})

@router.get("/detail/{id}")
async def detail_view(id: int, request: Request, detail_job: JobBoard = Depends(get_job_db)):
    job = await detail_job.retrieve_job(id=id)
    return templates.TemplateResponse("jobs/detail_view.html", {"request": request, "job": job})