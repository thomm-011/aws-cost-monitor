import boto3

def send_sns_alert(message, config, subject="AWS Cost Alert 🚨"):
    """
    Envia um alerta via SNS com base na configuração.

    Args:
        message (str): Conteúdo do alerta
        config (dict): Configurações carregadas do settings.json
        subject (str): Assunto do e-mail (padrão: AWS Cost Alert)
    """
    sns_topic_arn = config.get('sns_topic_arn')

    if not sns_topic_arn:
        print("❌ SNS Topic ARN não configurado no settings.json. Pulei envio de alerta.")
        return

    try:
        sns_client = boto3.client('sns')
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject=subject,
            Message=message
        )
        print(f"✅ Alerta enviado via SNS para o tópico: {sns_topic_arn}")

    except Exception as e:
        print(f"❌ Erro ao tentar enviar alerta SNS: {e}")
