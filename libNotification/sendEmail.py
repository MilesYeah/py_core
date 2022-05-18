import re
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error

from handlerLogger import logger


def send_email(smtp_server, smtp_port, from_email, password, to_list, subject, content, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = Header("Leo API Auto Test", 'utf-8')
        msg['To'] = ";".join(to_list)
        msg['Subject'] = Header(subject, 'utf-8')

        txt = MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)
        if attachment:
            # 添加附件
            part = MIMEApplication(open(attachment, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=attachment)
            msg.attach(part)

        # 设置服务器、端口
        s = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
        # 登录邮箱
        s.login(from_email, password)
        # 发送邮件
        s.send_message(msg, from_email, to_list)
        s.quit()
        return True, 'email send successfully'
    except smtplib.SMTPException as e:
        return False, 'SMTPException : %s' % str(e)
    except BaseException as e:
        return False, 'Exception : %s' % str(e)


class Email:
    """
    邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
    """

    def __init__(self, server, sender, password, receiver, title, message=None, files=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param files: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title
        self.message = message
        self.files = files

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open(f'{att_file}', 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))


if __name__ == '__main__':
    pass
