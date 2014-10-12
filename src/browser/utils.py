import hashlib
import re
import smtplib

from Crypto.Cipher import AES
from Crypto import Random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


kKey = 'datahub'

def encrypt_text (plain_text):
  key = hashlib.sha256(kKey).digest()
  iv = Random.new().read(AES.block_size)
  cipher = AES.new(key, AES.MODE_CFB, iv)
  crypt_text = (iv + cipher.encrypt(plain_text)).encode('hex')
  return crypt_text

def decrypt_text (crypt_text):
	iv_len = AES.block_size
	key = hashlib.sha256(kKey).digest()
	iv = crypt_text.decode('hex')[:iv_len]
	cipher = AES.new(key, AES.MODE_CFB, iv)
	plain_text = cipher.decrypt(crypt_text.decode('hex'))[iv_len:]
	return plain_text

def clean_str(text, prefix):
  s = text.strip().lower()
  
  # replace whitespace with '_'
  s = re.sub(' ', '_', s)
  
  # remove invalid characters
  s = re.sub('[^0-9a-zA-Z_]', '', s)

  # remove leading characters until a letter or underscore
  s = re.sub('^[^a-zA-Z_]+', '', s)

  if s == '':
    return clean_str(prefix + text, '')
  
  return s

def rename_duplicates(columns):
  columns = [c.lower() for c in columns]
  new_columns = []
  col_idx = {c:1 for c in columns}
  
  for c in columns:
    if columns.count(c) == 1:
      new_columns.append(c)
    else:
      # add a suffix
      new_columns.append(c + str(col_idx[c]))
      col_idx[c] += 1
  
  return new_columns

def send_email (addr, subject, msg_body):	
	email_subject = subject
	from_addr="datahub@csail.mit.edu"
	to_addr = [addr]
	
	msg = MIMEMultipart()
	msg['From'] = 'DataHub Team <datahub@csail.mit.edu>'
	msg['To'] = ",".join(to_addr)
	msg['Subject'] = email_subject
	msg.attach(MIMEText(msg_body))

	username = 'anantb'
	password = 'JcAt250486'
	smtp_conn = smtplib.SMTP_SSL('cs.stanford.edu', 465)
	smtp_conn.login(username, password)		
	smtp_conn.sendmail(from_addr, to_addr, msg.as_string())
	smtp_conn.close()