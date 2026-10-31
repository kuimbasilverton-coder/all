
from celery import shared_task
from django.core.mail import send_mail

from .models import Video


@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'silvertonkuimba@gmail.com',  # Replace with your email
        recipient_list,
        fail_silently=False,
    )

@shared_task
def long_task():
    # simulate a long-running task
    import time
    time.sleep(10)
    return 'Task complete'
    
    
    

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    # do something with the video, e.g., generate thumbnails
    print(f"Processing video {video.title}")    