from datetime import datetime
import json
import logging

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class EmailTrackerView(View):

    def get(self, request):
        validation_token = request.GET.get("validationToken")

        if validation_token:
            logger.info(f"[VALIDATION] Token received: {validation_token}")
            # ✅ Returns plain text directly — no CloudFront interfering
            return HttpResponse(
                validation_token,
                content_type="text/plain; charset=utf-8",
                status=200,
            )

        return HttpResponse(
            json.dumps({
                "status": "active",
                "message": "Webhook endpoint is active."
            }),
            content_type="application/json",
            status=200,
        )

    def post(self, request):
        raw_body = request.body
        logger.info(f"[WEBHOOK] Raw body: {raw_body}")

        if not raw_body:
            logger.info("[WEBHOOK] Empty body — lifecycle ping from Graph.")
            return HttpResponse(
                json.dumps({"status": "success"}),
                content_type="application/json",
                status=202,
            )

        try:
            data = json.loads(raw_body)
        except Exception as exc:
            logger.warning(f"[WEBHOOK] Parse error: {exc}")
            data = {}

        print("\n" + "📥" * 10)
        print("MICROSOFT GRAPH WEBHOOK RECEIVED")
        print(f"Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data : {data}")
        print("📥" * 10 + "\n")

        notifications = data.get("value", [])
        for notification in notifications:
            logger.info(
                f"[WEBHOOK] subscriptionId={notification.get('subscriptionId')} | "
                f"changeType={notification.get('changeType')} | "
                f"resource={notification.get('resource')}"
            )

        return HttpResponse(
            json.dumps({"status": "success"}),
            content_type="application/json",
            status=202,
        )
