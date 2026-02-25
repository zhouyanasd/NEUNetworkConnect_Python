import re
import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def get_rsa_password(text):
    # 网站使用的公钥
    pub_key_str = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKs2qmEOHBN7PF6O2M5UdvgLcs2tggpQ6gbypkz5mLFmWi8VCwyKM9guLhUu0TvolcrVvS9G51BOvJSKAsclJ3sCAwEAAQ=="
    
    # 构造标准 PEM 格式
    key_der = base64.b64decode(pub_key_str)
    public_key = RSA.import_key(key_der)
    
    # 使用 PKCS#1 v1.5 进行加密
    cipher = PKCS1_v1_5.new(public_key)
    # 加密内容为 用户名 + 密码
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    
    return base64.b64encode(encrypted_text).decode('utf-8')

url="https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_portal_sso%3Fac_id%3D1"
head={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Connection":"close",
    "Host": "pass.neu.edu.cn",
	"Referer": "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_portal_sso%3Fac_id%3D1",
    "Origin": "https://pass.neu.edu.cn",
    "Upgrade-Insecure-Requests": "1"
}
sess=requests.session()
res=sess.get(url,headers=head)

cookie = req.cookies

lt = re.search(r'name="lt" value="(.*?)"', res.text).group(1)
execution = re.search(r'name="execution" value="(.*?)"', res.text).group(1)
    
rsa_encrypted = get_rsa_password(stu_number + stu_pass)
    
payload = {
    "rsa": rsa_encrypted,
    "ul": str(len(stu_number)),
    "pl": str(len(stu_pass)),
    "lt": lt,
    "execution": execution,
    "_eventId": "submit"
}
r2=sess.post("https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_portal_sso%3Fac_id%3D1", headers=head, data=payload, 
             cookies=cookie, allow_redirects=False, verify=False)

Location = r2.headers['Location']
r2=sess.get(Location.replace('http://ipgw.neu.edu.cn/','http://ipgw.neu.edu.cn/v1/'),headers=head,cookies=cookie)

#---unnecessary----
# import numpy as np
# import time
# def produce_jQuery():
#     global jQuery
#     strnum = ""
#     for i in range(21):
#         strnum = strnum+str(int(np.random.uniform(0, 9)))
#     jQuery = "jQuery"+strnum+"_"

# produce_jQuery()
# callback = jQuery+str(int(time.time()*1000))

# r2=sess.get('http://ipgw.neu.edu.cn/cgi-bin/rad_user_info?callback='+callback,headers=head, cookies=cookie)
