from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from . import settings, api
from .models import Message
import json

@csrf_exempt
@require_http_methods(["POST"])
def callbackapi(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if body['type'] == 'confirmation':

        return HttpResponse(settings.VK_CONFIRMATION_KEY)

    elif body['type'] == 'message_new':
        user_id = body['object']['user_id']
        body = body['object']['body']

        message = Message(
            user_id = user_id,
            body = body,
            source = Message.SOURCE_VK
        )

        message.save()

        reply_body = "Записал: '{body}'".format(body=body)
        api.message_send(reply_body, user_id)

        return HttpResponse('ok')

