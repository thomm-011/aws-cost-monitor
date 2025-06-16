# AWS Cost Monitor 💰

Ferramenta Python para monitorar custos da AWS, gerar alertas automáticos e criar relatórios detalhados de gastos.

## 🎯 Funcionalidades

- 📊 **Monitoramento de custos** mensais e diários
- ⚠️ **Alertas automáticos** baseados em limites configuráveis
- 📈 **Comparação temporal** (mês atual vs anterior)
- 📄 **Relatórios exportáveis** (JSON, CSV)
- 🔧 **Configuração flexível** via arquivo JSON
- 💻 **Interface CLI** intuitiva

## 📂 Estrutura do Projeto

```
aws-cost-monitor/
├── src/
│   └── cost_analyzer.py      # Classe principal para análise de custos
├── config/
│   └── settings.json         # Configurações do projeto
├── reports/                  # Relatórios gerados automaticamente
├── requirements.txt          # Dependências Python
├── main.py                   # Script principal
└── README.md
```

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+**
- **Conta AWS** com permissões do Cost Explorer
- **Credenciais AWS** configuradas

### Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/thomm-011/aws-cost-monitor.git
   cd aws-cost-monitor
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure suas credenciais AWS:**
   ```bash
   # Opção 1: AWS CLI
   aws configure
   
   # Opção 2: Variáveis de ambiente
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

4. **Ajuste as configurações (opcional):**
   ```bash
   # O arquivo config/settings.json será criado automaticamente na primeira execução
   # Você pode editá-lo conforme necessário
   ```

## 💻 Como Usar

### Comandos Principais

```bash
# Relatório completo de custos mensais
python main.py --report

# Verificar apenas alertas de limite
python main.py --check-alerts

# Custos dos últimos N dias
python main.py --days 7

# Comparar mês atual com anterior
python main.py --compare
```

### Exemplos de Saída

**Relatório Completo:**
```
==================================================
🏆 AWS COST MONITOR
==================================================
💰 Custo Total: $45.67 USD
📅 Período: 2025-06-01 até 2025-06-15
🎯 Limite Mensal: $100.00
📊 Uso: 45.7%
📈 Status: ✅ Dentro do limite

🔝 TOP 5 SERVIÇOS:
----------------------------------------
1. EC2                 $   25.30 ( 55.4%)
2. S3                  $   12.45 ( 27.3%)
3. RDS                 $    5.67 ( 12.4%)
4. Lambda              $    1.89 (  4.1%)
5. CloudWatch          $    0.36 (  0.8%)
==================================================
```

**Alertas:**
```bash
python main.py --check-alerts
# Output: Status: ⚠️ CUIDADO: 80% do limite atingido
```

**Comparação Mensal:**
```bash
python main.py --compare
# Output: 
# 📊 Mês atual: $45.67
# 📊 Mês anterior: $38.92
# 📈 Variação: +17.3% (up)
```

## ⚙️ Configuração

O arquivo `config/settings.json` permite personalizar o comportamento da ferramenta:

```json
{
    "cost_limit_monthly": 100.00,      // Limite mensal em USD
    "alert_threshold": 0.8,            // Alerta quando atingir 80% do limite
    "currency": "USD",                 // Moeda padrão
    "email_alerts": false,             // Alertas por email (futuro)
    "report_format": ["json", "csv"]   // Formatos de relatório
}
```

### Parâmetros Explicados

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| `cost_limit_monthly` | Limite máximo de gastos mensais | 100.00 |
| `alert_threshold` | Percentual para disparar alertas (0.0-1.0) | 0.8 |
| `currency` | Moeda para exibição | "USD" |
| `email_alerts` | Ativar notificações por email | false |
| `report_format` | Formatos de relatório desejados | ["json", "csv"] |

## 🔐 Permissões AWS Necessárias

Sua conta AWS precisa das seguintes permissões:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetUsageReports"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📊 Relatórios

A ferramenta gera relatórios automáticos na pasta `reports/`:

- **JSON:** Estrutura completa dos dados para integração
- **CSV:** Formato tabular para análise em planilhas

Exemplo de nomenclatura: `cost_report_20250615_143022.json`

## 🚨 Sistema de Alertas

Alertas baseados no percentual do limite usado:

- ✅ **0-49%:** Dentro do limite
- 👀 **50-79%:** Metade do limite usado
- ⚠️ **80-89%:** Cuidado - 80% atingido
- ⚠️ **90-99%:** Alerta - Próximo do limite
- 🚨 **100%+:** Limite ultrapassado

## 🔧 Troubleshooting

### Problemas Comuns

**Erro de credenciais:**
```
NoCredentialsError: Unable to locate credentials
```
**Solução:** Configure suas credenciais AWS usando `aws configure`

**Erro de permissões:**
```
AccessDenied: User is not authorized to perform: ce:GetCostAndUsage
```
**Solução:** Adicione a política de Cost Explorer à sua conta

**Sem dados de custo:**
```
❌ Não foi possível obter dados de custo
```
**Solução:** Verifique se sua conta tem atividade de cobrança

### Logs e Debug

Para mais informações sobre erros, execute com verbose:
```bash
python main.py --report --verbose  # (implementar futuramente)
```

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License

## 📞 Contato

**Autor:** Thomas Silva  
**Email:** thomas.s.cordeiro@hotmail.com  
**LinkedIn:** https://www.linkedin.com/in/thomas-s-923082184/  
**GitHub:** https://github.com/thomm-011

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐