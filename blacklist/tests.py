from datetime import timedelta

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate, APIRequestFactory
from blacklist.models import PlayerReport, Game
from blacklist.views import PlayerReportViewSet


class PlayerTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'admin'
        self.password = 'test+password'

        self.user = User.objects.create_user(self.username, email='example@gamberban.co', password=self.password)

        admin_group, created = Group.objects.get_or_create(name='admin')

        player_report_content_type = ContentType.objects.get_for_model(PlayerReport)
        player_report_permissions = Permission.objects.filter(content_type=player_report_content_type)
        game_content_type = ContentType.objects.get_for_model(Game)
        game_permissions = Permission.objects.filter(content_type=game_content_type)

        admin_group.permissions.set(player_report_permissions | game_permissions)
        admin_group.user_set.add(self.user)

        admin_group.save()

        self.game1 = Game.objects.create(name='Game 1')
        self.game2 = Game.objects.create(name='Game 2')

        self.factory = APIRequestFactory()

    def test_create_player(self):

        data = {
            'email': 'player@example.com',
            'game': self.game1.id,
            'reason': 'CHEATING'
        }

        view = PlayerReportViewSet.as_view({'post': 'create'})

        request = self.factory.post('/blacklist/', data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_list_players(self):
        player1 = PlayerReport.objects.create(
            email='player1@example.com',
            game=self.game1,
            reason='CHEATING'
        )
        player2 = PlayerReport.objects.create(
            email='player2@example.com',
            game=self.game2,
            reason='CHEATING'
        )
        response = self.client.get('/blacklist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0], {
            'email': player1.email,
            'game': player1.game.id,
            'reason': player1.reason
        })
        self.assertEqual(response.data[1], {
            'email': player2.email,
            'game': player2.game.id,
            'reason': player2.reason
        })

    def test_create_player_without_required_fields(self):
        data = {}
        view = PlayerReportViewSet.as_view({'post': 'create'})

        request = self.factory.post('/blacklist/', data, format='json')

        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blacklist_players_more_than_90_days(self):
        now = timezone.now()
        ninety_days_ago = now - timedelta(days=91)
        player1 = PlayerReport.objects.create(
            email='player1@example.com',
            game=self.game1,
            reason='CHEATING',
        )
        player1.created_at = ninety_days_ago
        player1.save()
        player2 = PlayerReport.objects.create(
            email='player2@example.com',
            game=self.game2,
            reason='CHEATING'
        )
        response = self.client.get(f'/blacklist/check/?email={player1.email}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'most_commonly_reported_ban_reason': player1.reason,
            'times_reported_90_days': 0,
            'number_of_games_reported': 1,
        })

