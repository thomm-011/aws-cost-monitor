#!/usr/bin/env python3
"""
AWS Cost Monitor - Script Principal
Monitora custos da AWS e gera alertas
"""

import argparse
import json
import os
from datetime import datetime
from src.cost_analyzer import AWSCostAnalyzer

def load_config():
    """Carrega configurações do arquivo JSON"""
    config_path = 'config/settings.json'
    
    # Configuração padrão
    default_config = {
        "cost_limit_monthly": 100.00,
        "alert_threshold": 0.8,
        "currency": "USD",
        "email_alerts": False,
        "report_format": ["json", "csv"]
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}  # Merge com defaults
        else:
            # Criar arquivo de configuração padrão
            os.makedirs('config', exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Arquivo de configuração criado em: {config_path}")
            return default_config
            
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return default_config

def print_cost_report(cost_data, config):
    """Imprime relatório de custos no console"""
    if not cost_data:
        print("❌ Não foi possível obter dados de custo")
        return
    
    print("=" * 50)
    print("🏆 AWS COST MONITOR")
    print("=" * 50)
    
    total = cost_data['total']
    currency = config['currency']
    
    print(f"💰 Custo Total: ${total:.2f} {currency}")
    print(f"📅 Período: {cost_data['period']['Start']} até {cost_data['period']['End']}")
    
    # Verificar limite
    analyzer = AWSCostAnalyzer()
    limit_check = analyzer.check_cost_limit(config['cost_limit_monthly'], total)
    
    if limit_check:
        print(f"🎯 Limite Mensal: ${limit_check['limit']:.2f}")
        print(f"📊 Uso: {limit_check['percentage_used']:.1f}%")
        print(f"📈 Status: {limit_check['status']}")
    
    # Top 5 serviços
    if cost_data['services']:
        print("\n🔝 TOP 5 SERVIÇOS:")
        print("-" * 40)
        
        for i, service in enumerate(cost_data['services'][:5], 1):
            print(f"{i}. {service['name']:<20} ${service['cost']:>8.2f} ({service['percentage']:>5.1f}%)")
    
    print("=" * 50)

def generate_json_report(cost_data, filename):
    """Gera relatório em formato JSON"""
    try:
        os.makedirs('reports', exist_ok=True)
        filepath = f"reports/{filename}"
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'cost_summary': cost_data,
            'report_type': 'monthly_costs'
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4, default=str)
        
        print(f"📄 Relatório JSON salvo: {filepath}")
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório JSON: {e}")

def generate_csv_report(cost_data, filename):
    """Gera relatório em formato CSV"""
    try:
        import csv
        os.makedirs('reports', exist_ok=True)
        filepath = f"reports/{filename}"
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow(['Service', 'Cost', 'Percentage'])
            
            # Dados
            for service in cost_data['services']:
                writer.writerow([
                    service['name'],
                    f"{service['cost']:.2f}",
                    f"{service['percentage']:.1f}%"
                ])
            
            # Total
            writer.writerow(['', '', ''])
            writer.writerow(['TOTAL', f"{cost_data['total']:.2f}", '100.0%'])
        
        print(f"📊 Relatório CSV salvo: {filepath}")
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório CSV: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='AWS Cost Monitor')
    parser.add_argument('--report', action='store_true', 
                       help='Gerar relatório completo de custos')
    parser.add_argument('--check-alerts', action='store_true',
                       help='Apenas verificar alertas de limite')
    parser.add_argument('--days', type=int, default=None,
                       help='Custos dos últimos N dias')
    parser.add_argument('--compare', action='store_true',
                       help='Comparar com mês anterior')
    
    args = parser.parse_args()
    
    # Carregar configurações
    config = load_config()
    
    # Inicializar analisador
    analyzer = AWSCostAnalyzer()
    
    try:
        if args.days:
            # Custos diários
            print(f"📅 Obtendo custos dos últimos {args.days} dias...")
            daily_data = analyzer.get_daily_costs(args.days)
            
            if daily_data:
                print(f"💰 Total ({daily_data['period']}): ${daily_data['total']:.2f}")
                print(f"📊 Média diária: ${daily_data['total']/args.days:.2f}")
            
        elif args.compare:
            # Comparação mensal
            print("🔄 Comparando com mês anterior...")
            comparison = analyzer.compare_with_previous_month()
            
            if comparison:
                current = comparison['current_month']['total']
                previous = comparison['previous_month']['total']
                change = comparison['percentage_change']
                
                print(f"📊 Mês atual: ${current:.2f}")
                print(f"📊 Mês anterior: ${previous:.2f}")
                print(f"📈 Variação: {change:+.1f}% ({comparison['trend']})")
            
        elif args.check_alerts:
            # Apenas alertas
            print("⚠️  Verificando alertas...")
            cost_data = analyzer.get_monthly_costs()
            
            if cost_data:
                limit_check = analyzer.check_cost_limit(config['cost_limit_monthly'])
                if limit_check:
                    print(f"Status: {limit_check['status']}")
                    if limit_check['percentage_used'] >= config['alert_threshold'] * 100:
                        print("🚨 ALERTA ATIVADO!")
            
        else:
            # Relatório completo (padrão)
            print("📊 Gerando relatório de custos...")
            cost_data = analyzer.get_monthly_costs()
            
            if cost_data:
                # Mostrar no console
                print_cost_report(cost_data, config)
                
                # Gerar arquivos de relatório
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if 'json' in config['report_format']:
                    generate_json_report(cost_data, f'cost_report_{timestamp}.json')
                
                if 'csv' in config['report_format']:
                    generate_csv_report(cost_data, f'cost_report_{timestamp}.csv')
    
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        print("Verifique suas credenciais AWS e permissões do Cost Explorer")

if __name__ == '__main__':
    main()