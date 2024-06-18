import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

def check_alerts(df):
    for index, row in df.iterrows():
        if row['precio_usd'] > 10000:  # Ejemplo de umbral
            send_email(
                subject="Alerta de Precio",
                body=f"El precio de {row['nombre']} ha superado los 10000 USD. Precio actual: {row['precio_usd']} USD."
            )

if __name__ == "__main__":
    # Simular la transformación de datos
    from transform_data import transform_data
    from api_extraction import main as extract_data
    api_df, db_df = extract_data()
    combined_df = transform_data(api_df, db_df)
    
    check_alerts(combined_df)
