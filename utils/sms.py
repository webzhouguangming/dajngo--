# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
# 注意事项：
# 1.调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# 2.请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
# 3该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

from urllib.request import urlopen
from urllib.parse import urlencode
from django.conf import settings
import json


def send_sms_code(smscode, phone):

    # APIID(⽤户中⼼【验证码通知短信】-【产品纵览】查看)
    account = settings.APIID
    # APIKEY(⽤户中⼼【验证码通知短信】-【产品纵览】查看)
    password = settings.APIKEY
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。" % smscode
    data = {'account': account, 'password': password, 'content':
    text, 'mobile': phone, 'format': 'json'}
    req = urlopen(url='https://106.ihuyi.com/webservice/sms.php?method=Submit', data=urlencode(data).encode())
    content = req.read().decode()
    print(content)
    # code等于2代表提交成功，否则提交失败
    # smsid等于0代表提交失败，否则显示⻓度20流⽔号
    # b'{"code":2,"msg":"\xe6\x8f\x90\xe4\xba\xa4\xe6\x88\x90\xe5\x8a\x9f","smsid":"16063783563405105174"}'
    return json.loads(content)