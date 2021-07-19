from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from db.repository.jobs_data_access_layer import JobBoard
from schemas.jobs import JobCreate, ShowJob
from db.repository.jobs_data_access_layer import Job
from depends import get_job_db
from routes.route_login import get_current_user_from_token
from db.models.users import User

router = APIRouter()

@router.post("/create-job",response_model=ShowJob)
async def create_job(Job: JobCreate, jobs: Job = Depends(get_job_db), 
            current_user: User = Depends(get_current_user_from_token)):
    owner_id = current_user.id
    return await jobs.create_new_job(Job, owner_id)

@router.get("/get/{id}", response_model=ShowJob)
async def retrieve_job_by_id(id:int, id_job: JobBoard = Depends(get_job_db)):
    job_id = await JobBoard.retrieve_job(id_job, id=id)
    if not job_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    return job_id

@router.get("/all", response_model=List[ShowJob])
async def retrieve_all_jobs(all_jobs: JobBoard = Depends(get_job_db)):
    return await all_jobs.get_all_jobs()

@router.put("/update/{id}")
async def update_job(id: int, job: JobCreate, job_update: JobBoard = Depends(get_job_db), 
                current_user: User = Depends(get_current_user_from_token)):
    job_exist = await job_update.retrieve_job(id=id)
    if not job_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    if job_exist.owner_id == current_user.id or current_user.is_superuser:
        await job_update.update_job_by_id(id=id, job=job, owner_id=current_user.id)
        return {"detail": "Job Successfully updated"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You're not permitted to update this Job")

@router.delete("/delete/{id}")
async def delete_job(id: int, job_delete: JobBoard = Depends(get_job_db), 
                current_user: User = Depends(get_current_user_from_token)):
    job = await job_delete.retrieve_job(id=id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    if job.owner_id == current_user.id or current_user.is_superuser:
        await job_delete.delete_job_by_id(id=id, owner_id=current_user.id)
        return {"detail": "Job Successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You're not permitted to delete this Job")

