from core.app_celery import celery_app


@celery_app.task
def send_low_task_alert(product_id: int):
    return {"message": "Stock is low for the product with ID: {product_id}"}
