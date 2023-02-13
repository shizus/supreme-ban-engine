
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from blacklist.models import PlayerReport, Game
from blacklist.serializers import PlayerSerializer, GameSerializer


class PlayerReportViewSet(viewsets.ModelViewSet):
    """ Defines view behaviour for Player """
    queryset = PlayerReport.objects.all()
    serializer_class = PlayerSerializer
    authentication_classes = [JWTStatelessUserAuthentication]

    @action(detail=False, url_path='check')
    @swagger_auto_schema(
        authentication_classes=[JWTStatelessUserAuthentication],
        request_body=None,
        manual_parameters=[
            openapi.Parameter(
                name='email',
                in_='query',
                type='string',
                required=True,
                location='query',
                description='The email of the player'
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=openapi.Schema(
                    type='object',
                    properties={
                        'most_commonly_reported_ban_reason': openapi.Schema(
                            type='string',
                            description='The most commonly reported ban reason'
                        ),
                        'times_reported_90_days': openapi.Schema(
                            type='integer',
                            description='The number of times reported in the last 90 days'
                        ),
                        'number_of_games_reported': openapi.Schema(
                            type='integer',
                            description='The number of different games reported'
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description='Bad Request',
                schema=openapi.Schema(
                    type='object',
                    properties={
                        'error': openapi.Schema(
                            type='string',
                            description='Error message'
                        ),
                    }
                )
            ),
            404: openapi.Response(
                description='Player not found',
                schema=openapi.Schema(
                    type='object',
                    properties={
                        'detail': openapi.Schema(
                            type='string',
                            description='Error message'
                        ),
                    }
                )
            ),
        }
    )
    def check(self, request, format=None):
        """
        Check banned players based on email query parameter.

        This endpoint returns the most commonly reported ban reason, the number of times the player has been
        reported in the last 90 days, and the number of distinct games the player has been reported for.
        """
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        players = PlayerReport.objects.filter(email=email)

        if players.count() == 0:
            raise NotFound("Player not found.")

        most_commonly_reported_ban_reason = players.values('reason').annotate(
            count=Count('reason')).order_by('-count')[0]['reason']

        now = timezone.now()
        ninety_days_ago = now - timedelta(days=90)
        times_reported_90_days = players.filter(created_at__gte=ninety_days_ago).count()

        number_of_games_reported = players.values('game').distinct().count()

        return Response({
            'most_commonly_reported_ban_reason': most_commonly_reported_ban_reason,
            'times_reported_90_days': times_reported_90_days,
            'number_of_games_reported': number_of_games_reported,
        })


class GameViewSet(viewsets.ModelViewSet):
    """ Defines view behaviour for Player """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

