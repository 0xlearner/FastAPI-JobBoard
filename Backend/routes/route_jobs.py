from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from db.repository.job_board_dal import job_board
from schemas.jobs import JobCreate, ShowJob
from db.repository.job_board_dal import Job
from depends import get_db

router = APIRouter()

@router.post("/create-job",response_model=ShowJob)
async def create_user(Job: JobCreate, jobs: Job = Depends(get_db)):
    owner_id = 1
    return await jobs.create_new_job(Job, owner_id)

@router.get("/get/{id}", response_model=ShowJob)
async def retrieve_job_by_id(id:int, id_job: job_board = Depends(get_db)):
    job_id = await job_board.retrieve_job(id_job, id=id)
    if not job_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    return job_id

@router.get("/all", response_model=List[ShowJob])
async def retrieve_all_jobs(all_jobs: job_board = Depends(get_db)):
    return await all_jobs.get_all_jobs()

@router.put("/update/{id}")
async def update_job(id: int, job: JobCreate, job_update: job_board = Depends(get_db)):
    current_user = 1
    response = await job_update.update_job_by_id(id = id, job = job, owner_id = current_user)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    return {"response": "Successfully updated the Job."}

