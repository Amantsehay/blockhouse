from django.core.management.base import BaseCommand
from core.backtest import run_backtest
from core.tasks import get_stock_data
from core.report_generation import generate_report
from core.ml_price_prediction import prediction

class Command(BaseCommand):
    help = 'Run the trading strategy backtest'

    def handle(self, *args, **options):
        # result, trades, final_value  = run_backtest('AAPL', 1000)
        # report = generate_report(result, 1000, final_value, trades)
        result = prediction.test()
        print(result)
    
        # print(result)
        # result = get_stock_data('AAPL')
        # print(final_value)
        # print(result)
        
        # self.stdout.write(str(result))
