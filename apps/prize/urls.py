from django.urls import path

from apps.prize.api.prize_redemption_api import PrizeRedemptionAPi


urlpatterns_api = [
    path('prize-redemption/', PrizeRedemptionAPi.as_view(), name='post_prize_redemption'),
]