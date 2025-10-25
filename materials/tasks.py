from celery import shared_task
from django.core.mail import send_mail
from .models import Course

@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = course.subscriptions.all()
    
    for subscription in subscribers:
        send_mail(
            f'Обновление курса {course.title}',
            f'Курс {course.title} был обновлен. Проверьте новые материалы!',
            'admin@lms.ru',
            [subscription.user.email],
            fail_silently=False,
        )