from rest_framework.views import APIView
from .tasks import store_tweets
from .serializers import TweetSerializer
from rest_framework.response import Response

class tweet(APIView):
    def get(self, request):
        tweets = store_tweets()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)