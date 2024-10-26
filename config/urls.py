# urls.py
from django.contrib import admin
from django.urls import path
from core.views import EMAStrategyView, FetchStockDataView, PredictStockPriceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ema-strategy/', EMAStrategyView.as_view(), name='ema-strategy'),
    path('api/fetch-stock-data/', FetchStockDataView.as_view(), name='fetch-stock-data'),
    path('api/predict-future-price/', PredictStockPriceView.as_view(), name='predict-future-price')
]
