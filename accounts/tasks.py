from celery import shared_task
# from userManagement.celery import celery_app
from SMTP.utils.send_mail import send_email
from accounts.utils import get_activation_url


@shared_task
# @celery_app.task
def send_activation_mail(instance):
    msg = format_msg(instance)
    send_email([instance.email], msg)


def format_msg(instance):
    activation_link = get_activation_url(instance)
    print("activation link", activation_link)
    msg = '<div>' \
          ' <div>' \
          '<img src="" alt="Loading..">' \
          '</div>' \
          '<div style="color:\'white\'">' \
          '   Hi {},' \
          'Please click on the button to complete the verification process for xxxxxx@xxxx.xxx:' \
          ' <a href="{}" alt="Error in link">Click here </a>' \
          '</div>' \
          '<div style="color:\'gray\'">' \
          '   If you didn\'t attempt to verify your email address with our service, delete this email.' \
          '  Thanks & Regards,' \
          ' Energy Harbors corporation PVT LTD' \
          'Bangalore - India' \
          '</div>' \
          '</div> '.format(instance.first_name, activation_link)
    print("msg>>>>>", msg)
    return msg
