from celery.decorators import task
from celery.utils.log import get_task_logger

from time import sleep

from apps.authentication.celery.send_mail import send_confirmation_email

logger = get_task_logger(__name__)


@task(name='send_notification_task')
def send_notification_task(user, seconds):
    is_task_completed = False
    try:
        sleep(seconds)
        is_task_completed = True
    except Exception as err:
        error = str(err)
        logger.error(error)
    if is_task_completed:
        send_confirmation_email(user)
    return 'my_task_done!!!!!!'

