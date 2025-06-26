# AWS Cost Monitor 💰

Ferramenta Python para monitorar custos da AWS, gerar alertas automáticos e criar relatórios detalhados de gastos.

## 🎯 Funcionalidades

- 📊 **Monitoramento de custos** mensais e diários via Cost Explorer API
- ⚠️ **Alertas automáticos** baseados em limites configuráveis
- 📈 **Comparação temporal** (mês atual vs anterior)
- 📄 **Relatórios exportáveis** (JSON, CSV)
- 🔧 **Configuração flexível** via arquivo JSON
- 💻 **Interface CLI** intuitiva

---

## 🚀 Tecnologias Usadas

- Python 3.8+
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) (SDK AWS)
- AWS Cost Explorer API (`ce:GetCostAndUsage`)
- Futuro: Amazon SNS ou SES para envio de alertas por e-mail

---

## 📂 Estrutura do Projeto

aws-cost-monitor/
├── src/
│ └── cost_monitor.py # Lógica principal do monitor
├── config/
│ └── settings.json # Configurações do projeto
├── reports/ # Relatórios gerados automaticamente
├── requirements.txt # Dependências Python
├── main.py # Script CLI principal
└── README.md


---

## 🛠️ Instalação

### Pré-requisitos

- **Python 3.8+**
- **Conta AWS** com permissões do Cost Explorer ativado
- **Credenciais AWS** válidas e configuradas

### Passos

```bash
# Clone o projeto
git clone https://github.com/thomm-011/aws-cost-monitor.git
cd aws-cost-monitor

# Instale as dependências
pip install -r requirements.txt

# Configure suas credenciais AWS
aws configure  # ou via variáveis de ambiente

💻 Como Usar

# Gerar relatório completo
python main.py --report

# Checar status de alerta
python main.py --check-alerts

# Custos dos últimos 7 dias
python main.py --days 7

# Comparar mês atual com o anterior
python main.py --compare

🧾 Exemplo de Saída

🏆 AWS COST MONITOR
💰 Total: $45.67 USD
📅 Período: 2025-06-01 até 2025-06-15
🎯 Limite Mensal: $100.00
📊 Uso: 45.7%
📈 Status: ✅ Dentro do limite

🔝 TOP 5 SERVIÇOS:
1. EC2 ........... $25.30
2. S3 ............ $12.45
3. RDS ........... $5.67
4. Lambda ........ $1.89
5. CloudWatch .... $0.36

⚙️ Configuração (config/settings.json)

{
  "cost_limit_monthly": 100.00,
  "alert_threshold": 0.8,
  "currency": "USD",
  "email_alerts": false,
  "report_format": ["json", "csv"]
}

Parâmetro	Descrição	Valor Padrão
cost_limit_monthly	Limite máximo de gastos mensais (USD)	100.00
alert_threshold	Percentual para acionar alerta (0.0–1.0)	0.8
email_alerts	Ativar alertas por email (futuro)	false
report_format	Formatos gerados (json, csv)	["json", "csv"]


📜 Permissões AWS Recomendadas

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetUsageForecast"
      ],
      "Resource": "*"
    }
  ]
}

🚨 Sistema de Alertas
Nível de Uso	Status
0–49%	✅ Dentro do limite
50–79%	👀 Atenção
80–89%	⚠️ Cuidado
90–99%	⚠️ Alerta
100%+	🚨 Limite atingido
📊 Relatórios

    JSON: estrutura completa para integração

    CSV: leitura facilitada por planilhas

    Geração automática na pasta reports/ ex:
        cost_report_20250615_143022.json

🔍 Troubleshooting

Erro de credenciais

NoCredentialsError: Unable to locate credentials

→ Solução: execute aws configure

Erro de permissão

AccessDenied: User is not authorized to perform: ce:GetCostAndUsage

→ Solução: adicione as permissões acima à IAM
🗺️ Roadmap Futuro

Relatórios diários/mensais

Alertas baseados em percentual de uso

Integração com Amazon SNS (alertas por email)

Agendamento com Lambda ou CloudWatch Events

Exportação em PDF (via ReportLab)

Interface web (opcional)

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