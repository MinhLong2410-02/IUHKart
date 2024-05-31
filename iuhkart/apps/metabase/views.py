from django.conf import settings
import jwt, time
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
METABASE_SITE_URL = settings.METABASE_SITE_URL
METABASE_EMBEDDING_SECRET_KEY = settings.METABASE_EMBEDDING_SECRET_KEY


def getDashboardFromVendorId(vendor_id):
    payload = {
        "resource": {"dashboard": 2},
        "params": {
            "id": vendor_id
        },
        "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_EMBEDDING_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=false"
    return iframeUrl

class MetabaseDashboardView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            vendor_id = request.user.vendor.id
            dashboard_url = getDashboardFromVendorId(vendor_id)
            return Response({"iframeUrl": dashboard_url})
        except ObjectDoesNotExist:
            return Response({"error": "User is not associated with a vendor"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)