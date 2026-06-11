from fastapi import APIRouter

router = APIRouter(
    prefix="/runs",
    tags=["runs"])

mock = 'mock'

@router.post("")
async def create_run():
    #payload: RunCreate (в скобах)
    return [mock]  

@router.get("")
async def get_runs():
    return [mock]  

@router.get("/{run_id}")
async def get_run(run_id: str):
    return [mock]  

@router.get("/{run_id}/result")
async def get_result(run_id: str):
    return [mock]  

  