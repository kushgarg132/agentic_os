from .celery_app import celery_app

@celery_app.task
def daily_summary_task(user_id: int):
    # Logic to generate daily summary
    print(f"Generating daily summary for user {user_id}")
    pass

@celery_app.task
def index_drive_task(user_id: int):
    # Logic to index Drive files
    print(f"Indexing Drive for user {user_id}")
    pass
