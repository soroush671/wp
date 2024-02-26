import requests
import json

url = "http://vnapishz.zagros-grp.com:9096/api/ThirdPartyOrderAPI/CreateOrder?actiontype=1"

# ایجاد لیستی از دیکشنری‌ها که معادل orderitems است
orderitems = []
for item in session['cart']:
    orderitems.append({
        "ReferenceKey": "",
        "ReferenceNo": "",
        "OrderDate": "1402/11/29",
        "StockId": 1,
        "OrderTypeId": 2,
        "CustomerId": 50034081,
        "PaymentUsanceId": 1,
        "SalesmanId": 2974,
        "OrderComment": "test",
        "ProductId": item['product_id'],
        "BatchNoId": "",
        "Quantity": item['quantity'],
        "ItemComment": "",
        "DisTypeId": 2,
        "FreightAmount": None,
        "UnitPrice": None,
        "Dis1Amount": None,
        "Dis2Amount": None,
        "Dis3Amount": None,
        "Add1Amount": None,
        "Add2Amount": None
    })

# تبدیل orderitems به json و ارسال به سرور
payload = json.dumps({"orderitems": orderitems})
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJ1c2VybmFtZSI6InZhcmFuZWdhciIsImZ1bGxuYW1lIjoi2YjYsdin2Ybar9ixIiwibmJmIjoxNzAzOTE1NDI2LCJleHAiOjE3MDY1MDc0MjYsImlhdCI6MTcwMzkxNTQyNiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo0NDM4NSIsImF1ZCI6InRoaXJkcGFydHlVc2VyIn0.djVWn5971u92HwgMZpV9aZ8_AA9y3UE0c9Dnj-GqiaM',
    'AccYear': '1401',
    'CenterId': '3',
    'SaleOfficeId': '1',
    'Language': 'en',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
