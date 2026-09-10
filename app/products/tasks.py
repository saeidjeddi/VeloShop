from celery import shared_task


@shared_task
def update_products():
    print("🚀 Updating products...")
    return "Products updated"