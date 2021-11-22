from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr


from_addr = 'ren_jinbo@163.com'

with open('C:\\Users\\Administrator\\Documents\\pyTest\\pypw.txt','r', encoding='utf-8') as f:
	fromword = f.readlines()[0]

to_addr = "ren.jinbo@navercorp.com"
# to_addr = "ren_jinbo@163.com"

smtp_server = 'smtp.163.com'

def  _formata_addr(s):
	nama, addr = parseaddr(s)
	return formataddr((Header(nama, 'utf-8').encode(), addr))

msg = MIMEText('这是正文内容', 'plain', 'utf-8')
msg['Subject'] = Header("必须有个主题", 'utf-8')
# msg['From'] =Header("发送测试人员", 'utf-8')
msg['From'] = _formata_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _formata_addr('Python爱好者接收 <%s>' % from_addr)
# msg['To'] = "你好的管理员"



import smtplib

server = smtplib.SMTP()
server.connect(smtp_server)
server.set_debuglevel(1)
server.login(from_addr, fromword)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit
