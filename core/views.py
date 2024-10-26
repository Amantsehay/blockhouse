import logging
from numpy import short
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.serializer import EMAStrategySerializer, FetchStockDataSerializer, PredictStockPriceSerializer
from core.backtest import run_backtest
from core.report_generation import generate_report
from core.utils.model_loader import load_model
from core.ml_price_prediction.prediction import StockPricePredictor

from .models import StockModel, PredictedPriceModel
from .tasks import fetch_stock_data

logger = logging.getLogger(__name__)  # Set up logging

class EMAStrategyView(APIView):
    def post(self, request):
        serializer = EMAStrategySerializer(data=request.data)
        if serializer.is_valid():
            short_window = serializer.validated_data['short_window']
            long_window = serializer.validated_data['long_window']
            stock_symbol = serializer.validated_data['stock_symbol']
            initial_investment = serializer.validated_data['initial_investment']

            try:
                data, trades, final_value = run_backtest(stock_symbol, initial_investment=initial_investment, short_window=short_window, long_window=long_window)
                final_report = generate_report(data, initial_investment, final_value, trades)
                
                return Response({
                    'message': 'Backtest completed successfully',
                    'final_value': final_value,
                    'report': final_report
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error during backtest: {str(e)}")  # Log the error
                return Response({'error': 'An error occurred while running the backtest.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FetchStockDataView(APIView):
    def post(self, request):
        serializer = FetchStockDataSerializer(data=request.data)
        if serializer.is_valid():
            stock_symbol = serializer.validated_data["stock_symbol"]
            message, status_code = fetch_stock_data(stock_symbol)
            
            return Response({"message": message}, status=status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PredictStockPriceView(APIView):
    def post(self, request):
        serializer = PredictStockPriceSerializer(data=request.data)
        if serializer.is_valid():
            stock_symbol = serializer.validated_data["stock_symbol"]

            predictor = StockPricePredictor(stock_symbol=stock_symbol)

            try:
                predictions = predictor.predict_future_prices()

                # Save predictions to the database
                for date, row in predictions.iterrows():
                    try:
                        PredictedPriceModel.objects.create(
                            symbol=stock_symbol,
                            date=date,
                            predicted_price=row['Predicted Price']
                        )
                    except IntegrityError as e:
                        logger.warning(f"Integrity error while saving prediction for {stock_symbol} on {date}: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error saving prediction: {str(e)}")

                predictions_dict = predictions.copy()
                predictions_dict.index = predictions_dict.index.astype(str) 
                predictions_dict.reset_index(inplace=True)  
                return Response({
                    'message': 'Predictions generated successfully',
                    'predictions': predictions_dict.to_dict(orient='records')
                }, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")  # Log the error
                return Response({'error': 'An error occurred while generating predictions.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
