from app.scheduled.models import ImportJobId
from app.scheduled.scheduler import scheduler


def increase_cursor(job_id: ImportJobId):
    job = scheduler.get_job(job_id.value)
    cursor = job.kwargs["cursor"]
    cursor["batch_id"] = cursor["batch_id"] + job.kwargs["n_batches"]
    job.kwargs["cursor"] = cursor
    job.modify(kwargs=job.kwargs)
