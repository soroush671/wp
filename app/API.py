import requests


def send_verification_code(phone_number, token):



    url = (f"http://api.payamak-panel.com/post/Send.asmx/SendSimpleSMS2?username=zagroszarin&password"
           f"=ZagrosVNSMS&to={phone_number}&from=1000000037073&text=شرکت پخش زاگرس کد تائید :{token}&isflash=true")

    payload = {}
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
