import importlib.util
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.cost_monitor import AWSCostMonitor


class CostMonitorTests(unittest.TestCase):
    def setUp(self):
        with patch('src.cost_monitor.boto3.client') as create:
            self.monitor = AWSCostMonitor()
            self.client = create.return_value

    def test_grouped_response_without_total_preserves_credits(self):
        response = {'ResultsByTime': [{
            'TimePeriod': {'Start': '2026-10-01', 'End': '2026-11-01'},
            'Total': {},
            'Groups': [
                {'Keys': ['Amazon EC2'], 'Metrics': {'BlendedCost': {'Amount': '20.25', 'Unit': 'USD'}}},
                {'Keys': ['Credit'], 'Metrics': {'BlendedCost': {'Amount': '-5.25', 'Unit': 'USD'}}}
            ]
        }]}
        result = self.monitor._process_cost_data(response)
        self.assertEqual(result['total'], 15.0)
        self.assertEqual(sum(x['cost'] for x in result['services']), 15.0)
        self.assertEqual(result['period']['End'], '2026-11-01')

    def test_zero_cost_does_not_request_new_data(self):
        self.monitor.get_monthly_costs = Mock()
        result = self.monitor.check_cost_limit(100, current_cost=0)
        self.assertEqual(result['percentage_used'], 0)
        self.monitor.get_monthly_costs.assert_not_called()

    def test_empty_month_period_is_zero_without_aws_call(self):
        result = self.monitor.get_monthly_costs('2026-11-01', '2026-11-01')
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['services'], [])
        self.client.get_cost_and_usage.assert_not_called()

    def test_previous_month_includes_its_last_day(self):
        with patch('src.cost_monitor.datetime') as clock:
            clock.now.return_value = datetime(2026, 1, 15)
            self.monitor.get_monthly_costs = Mock(return_value={'total': 10})
            self.monitor.compare_with_previous_month()
        self.assertEqual(self.monitor.get_monthly_costs.call_args_list[1].args,
                         ('2025-12-01', '2026-01-01'))

    def test_cli_module_imports_existing_monitor(self):
        spec = importlib.util.spec_from_file_location('cost_cli', Path(__file__).parents[1] / 'main.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIs(module.AWSCostMonitor, AWSCostMonitor)


if __name__ == '__main__':
    unittest.main()
