import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate
import logging
from typing import Dict, List, Union

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# SMTP-серверы для разных почтовых сервисов
SMTP_SERVERS = {
    'gmail.com': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'ssl_port': 465
    },
    'mail.ru': {
        'server': 'smtp.mail.ru',
        'port': 587,
        'ssl_port': 465
    },
    'yandex.ru': {
        'server': 'smtp.yandex.ru',
        'port': 587,
        'ssl_port': 465
    },
    'yandex.com': {
        'server': 'smtp.yandex.com',
        'port': 587,
        'ssl_port': 465
    },
    'outlook.com': {
        'server': 'smtp.office365.com',
        'port': 587,
        'ssl_port': None
    },
    'hotmail.com': {
        'server': 'smtp.office365.com',
        'port': 587,
        'ssl_port': None
    },
    'default': {
        'server': 'smtp.{domain}',
        'port': 587,
        'ssl_port': 465
    }
}

class EmailSender:
    def __init__(self, sender_email: str, sender_password: str):
        """
        Инициализация отправителя
        :param sender_email: Email отправителя
        :param sender_password: Пароль или токен приложения
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.domain = sender_email.split('@')[-1].lower()
        self.smtp_info = SMTP_SERVERS.get(self.domain, SMTP_SERVERS['default'])
        
        # Подставляем домен в сервер, если нужно
        if '{domain}' in self.smtp_info['server']:
            self.smtp_info['server'] = self.smtp_info['server'].format(domain=self.domain)

    def _create_message(
        self,
        recipient_email: str,
        subject: str,
        message: str,
        is_html: bool = False,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None
    ) -> MIMEMultipart:
        """Создание MIME-сообщения"""
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Sender', self.sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        
        # BCC не добавляется в заголовки, получатели не видят друг друга
        if is_html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))
        
        return msg

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        message: str,
        is_html: bool = False,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None,
        retries: int = 2
    ) -> bool:
        """
        Отправка одного email
        :param recipient_email: Email получателя
        :param subject: Тема письма
        :param message: Текст письма
        :param is_html: HTML-формат сообщения
        :param cc_emails: Список email для копии
        :param bcc_emails: Список email для скрытой копии
        :param retries: Количество попыток отправки
        :return: Успешность отправки
        """
        msg = self._create_message(recipient_email, subject, message, is_html, cc_emails, bcc_emails)
        recipients = [recipient_email]
        if cc_emails:
            recipients.extend(cc_emails)
        if bcc_emails:
            recipients.extend(bcc_emails)

        last_exception = None
        
        for attempt in range(retries):
            try:
                # Пробуем STARTTLS (порт 587)
                if self.smtp_info['port']:
                    try:
                        with smtplib.SMTP(self.smtp_info['server'], self.smtp_info['port']) as server:
                            server.starttls(context=ssl.create_default_context())
                            server.login(self.sender_email, self.sender_password)
                            server.sendmail(self.sender_email, recipients, msg.as_string())
                            logger.info(f"Email sent to {recipient_email} via {self.smtp_info['server']}:{self.smtp_info['port']}")
                            return True
                    except Exception as e:
                        last_exception = e
                        logger.warning(f"Attempt {attempt + 1} failed (STARTTLS): {str(e)}")

                # Пробуем SSL (порт 465)
                if self.smtp_info['ssl_port']:
                    try:
                        with smtplib.SMTP_SSL(
                            self.smtp_info['server'],
                            self.smtp_info['ssl_port'],
                            context=ssl.create_default_context()
                        ) as server:
                            server.login(self.sender_email, self.sender_password)
                            server.sendmail(self.sender_email, recipients, msg.as_string())
                            logger.info(f"Email sent to {recipient_email} via {self.smtp_info['server']}:{self.smtp_info['ssl_port']}")
                            return True
                    except Exception as e:
                        last_exception = e
                        logger.warning(f"Attempt {attempt + 1} failed (SSL): {str(e)}")

                time.sleep(2 ** attempt)  # Экспоненциальная задержка

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error: {str(e)}")
                time.sleep(2 ** attempt)

        logger.error(f"Failed to send email to {recipient_email} after {retries} attempts. Last error: {str(last_exception)}")
        return False

    def send_bulk_emails(
        self,
        recipients: Union[List[str], Dict[str, str]],
        subject: str,
        message_template: str,
        is_html: bool = False,
        delay: float = 1.0,
        batch_size: int = 50,
        batch_delay: float = 60.0
    ) -> Dict[str, bool]:
        """
        Массовая рассылка emails
        :param recipients: Список email или словарь {email: name}
        :param subject: Тема письма
        :param message_template: Шаблон сообщения (может содержать {name})
        :param is_html: HTML-формат сообщения
        :param delay: Задержка между отправками (в секундах)
        :param batch_size: Размер пачки перед большой задержкой
        :param batch_delay: Большая задержка после пачки (в секундах)
        :return: Словарь с результатами {email: success}
        """
        if isinstance(recipients, list):
            recipients = {email: '' for email in recipients}

        results = {}
        total_sent = 0

        for i, (email, name) in enumerate(recipients.items()):
            try:
                personalized_msg = message_template.format(name=name) if name else message_template
                success = self.send_email(email, subject, personalized_msg, is_html)
                results[email] = success
                
                if success:
                    total_sent += 1
                    logger.info(f"Progress: {total_sent}/{len(recipients)} emails sent")

                # Регулярные задержки
                if i < len(recipients) - 1:
                    time.sleep(delay)

                # Большая задержка после batch_size писем
                if (i + 1) % batch_size == 0:
                    logger.info(f"Sent {i + 1} emails. Waiting {batch_delay} seconds...")
                    time.sleep(batch_delay)

            except Exception as e:
                logger.error(f"Error processing email {email}: {str(e)}")
                results[email] = False
                time.sleep(delay * 2)  # Увеличиваем задержку при ошибке

        success_rate = (sum(results.values()) / len(results)) * 100
        logger.info(f"Bulk sending completed. Success rate: {success_rate:.2f}%")
        return results
    

sender = EmailSender(
sender_email="mannanovr70@gmail.com",
sender_password="oafd mldn jpqj lgxk"  # Для Gmail нужен пароль приложений
)

# 2. Отправка тестового письма
sender.send_email(
    recipient_email="sai.radmir@yandex.ru",
    subject="Тестовое письмо",
    message="Привет! Это тестовое письмо из Python.",
    is_html=False
)


# 3. Массовая рассылка с персонализацией
recipients = {
    "user1@example.com": "Алексей",
    "user2@mail.ru": "Мария",
    "user3@yandex.ru": "Иван"
}

html_template = """
<html>
  <body>
    <h1>Привет, {name}!</h1>
    <p>Это персонализированное письмо из нашей рассылки.</p>
    <p>С уважением,<br>Команда проекта</p>
  </body>
</html>
"""

results = sender.send_bulk_emails(
    recipients=recipients,
    subject="Персональное предложение",
    message_template=html_template,
    is_html=True,
    delay=2.0,
    batch_size=20,
    batch_delay=120.0
)