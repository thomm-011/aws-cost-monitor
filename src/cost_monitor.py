import boto3
import json
from datetime import datetime, timedelta
from decimal import Decimal

class AWSCostMonitor:
    def __init__(self):
        """Inicializa o analisador de custos AWS"""
        self.client = boto3.client('ce')  # Cost Explorer
        self.currency = 'USD'
        
    def get_monthly_costs(self, start_date=None, end_date=None):
        """
        Obtém os custos mensais da AWS
        
        Args:
            start_date (str): Data início (YYYY-MM-DD)
            end_date (str): Data fim (YYYY-MM-DD)
            
        Returns:
            dict: Dados de custo organizados
        """
        if not start_date:
            # Primeiro dia do mês atual
            today = datetime.now()
            start_date = today.replace(day=1).strftime('%Y-%m-%d')
            
        if not end_date:
            # Hoje
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        if start_date == end_date:
            return self._process_cost_data({'ResultsByTime': []}, {'Start': start_date, 'End': end_date})

        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                GroupBy=[{
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }]
            )
            
            return self._process_cost_data(response, {'Start': start_date, 'End': end_date})
            
        except Exception as e:
            print(f"Erro ao consultar custos: {e}")
            return None
    
    def get_daily_costs(self, days=7):
        """
        Obtém custos diários dos últimos N dias
        
        Args:
            days (int): Número de dias para consultar
            
        Returns:
            dict: Custos diários
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost']
            )
            
            daily_costs = []
            for result in response['ResultsByTime']:
                date = result['TimePeriod']['Start']
                amount = float(result['Total']['BlendedCost']['Amount'])
                daily_costs.append({
                    'date': date,
                    'cost': amount
                })
                
            return {
                'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                'daily_costs': daily_costs,
                'total': sum(day['cost'] for day in daily_costs)
            }
            
        except Exception as e:
            print(f"Erro ao consultar custos diários: {e}")
            return None
    
    def _process_cost_data(self, response, period=None):
        """Normalize totals and grouped service costs without requiring Total in grouped responses."""
        results = response.get('ResultsByTime', [])
        service_costs = {}
        total = Decimal('0')
        currency = self.currency
        for result in results:
            groups = result.get('Groups', [])
            grouped_total = Decimal('0')
            for group in groups:
                metric = group.get('Metrics', {}).get('BlendedCost', {})
                amount = Decimal(metric.get('Amount', '0'))
                currency = metric.get('Unit', currency)
                grouped_total += amount
                name = group['Keys'][0]
                service_costs[name] = service_costs.get(name, Decimal('0')) + amount
            metric = result.get('Total', {}).get('BlendedCost')
            if metric is not None:
                total += Decimal(metric['Amount'])
                currency = metric.get('Unit', currency)
            else:
                total += grouped_total
        services = [
            {'name': name, 'cost': float(cost),
             'percentage': float(cost / total * 100) if total else 0.0}
            for name, cost in service_costs.items() if cost != 0
        ]
        services.sort(key=lambda item: item['cost'], reverse=True)
        if results:
            period = {'Start': results[0]['TimePeriod']['Start'],
                      'End': results[-1]['TimePeriod']['End']}
        return {'total': float(total), 'currency': currency, 'services': services,
                'period': period or {'Start': '', 'End': ''}}

    def compare_with_previous_month(self):
        """
        Compara custos do mês atual com o anterior
        
        Returns:
            dict: Comparação de custos
        """
        # Mês atual
        today = datetime.now()
        current_start = today.replace(day=1)
        current_end = today
        
        # Mês anterior
        if current_start.month == 1:
            previous_start = current_start.replace(year=current_start.year - 1, month=12)
        else:
            previous_start = current_start.replace(month=current_start.month - 1)
            
        # Cost Explorer uses an exclusive end date: the first day of this month.
        previous_end = current_start

        # Buscar custos
        current_costs = self.get_monthly_costs(
            current_start.strftime('%Y-%m-%d'),
            current_end.strftime('%Y-%m-%d')
        )
        
        previous_costs = self.get_monthly_costs(
            previous_start.strftime('%Y-%m-%d'),
            previous_end.strftime('%Y-%m-%d')
        )
        
        if not current_costs or not previous_costs:
            return None
            
        # Calcular diferença
        difference = current_costs['total'] - previous_costs['total']
        percentage_change = (difference / previous_costs['total'] * 100) if previous_costs['total'] > 0 else 0
        
        return {
            'current_month': current_costs,
            'previous_month': previous_costs,
            'difference': difference,
            'percentage_change': percentage_change,
            'trend': 'up' if difference > 0 else 'down' if difference < 0 else 'stable'
        }
    
    def check_cost_limit(self, limit, current_cost=None):
        """
        Verifica se os custos ultrapassaram o limite
        
        Args:
            limit (float): Limite de custo
            current_cost (float): Custo atual (opcional)
            
        Returns:
            dict: Status do limite
        """
        if current_cost is None:
            current_data = self.get_monthly_costs()
            if not current_data:
                return None
            current_cost = current_data['total']
        
        percentage_used = (current_cost / limit * 100) if limit > 0 else 0
        
        return {
            'current_cost': current_cost,
            'limit': limit,
            'percentage_used': percentage_used,
            'over_limit': current_cost > limit,
            'status': self._get_status_message(percentage_used)
        }
    
    def _get_status_message(self, percentage):
        """
        Retorna mensagem de status baseada na porcentagem usada
        
        Args:
            percentage (float): Porcentagem do limite usada
            
        Returns:
            str: Mensagem de status
        """
        if percentage >= 100:
            return "🚨 LIMITE ULTRAPASSADO!"
        elif percentage >= 90:
            return "⚠️  ALERTA: Próximo do limite!"
        elif percentage >= 80:
            return "⚠️  CUIDADO: 80% do limite atingido"
        elif percentage >= 50:
            return "👀 Metade do limite usado"
        else:
            return "✅ Dentro do limite"