from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, F, Q
from account.models import User
from .models import TextGenHistory
from django.utils import timezone
import datetime

class RankingGenerateAPIView(APIView):
    def get(self, request):
        weekago = timezone.now() - datetime.timedelta(days=7)
        query = TextGenHistory.objects.filter(gen_date__gt=weekago).filter(~Q(target_user=F('request_from')) | Q(request_from__isnull=True)).values('target_user').annotate(count=Count('target_user')).order_by('count').reverse()[:10]
        result = []
        for q in query:
            user = User.objects.filter(id=q['target_user']).first()
            result.append({ 'screen_name': user.screen_name, 'count': q['count'] })
        return Response(result)
