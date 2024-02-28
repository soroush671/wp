from app import sql_server_cursor
from app.models import User, Brand
import requests
import json


def user_finder(user_id):
    sql_server_query = f"SELECT * FROM Zagros_Customer2 WHERE [کد مشتری]='{user_id}'"
    result = sql_server_cursor.execute(sql_server_query).fetchall()
    if result:
        user_data = result[0]  # گرفتن اولین رکورد از نتیجه
        mobile_number = user_data[5]  # فرضاً موبایل در ستون ششم قرار دارد
        user_id = user_data[0]
        shop_name = user_data[2]
        customer_id = user_data[30]

        return User(username=user_id, password=mobile_number, shop_name=shop_name, customer_id=customer_id)
    else:
        return None


def brand_finder():
    brand = Brand.query.all()
    return brand


def good_list_finder():
    sql_server_query =(f"SELECT Zagros_Goods.*,"
                       " Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن],"
                       "Zagros_StockGoods.[شناسه کالا]FROM Zagros_Goods"
                       " JOIN Zagros_StockGoods ON Zagros_Goods.[کد کالا] = Zagros_StockGoods.[کد کالا]"
                       " WHERE Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن] "
                       "IS NOT NULL AND [مرکز توزیع]='شیراز' and [نام تجاری] ='Persil' ")

    result = sql_server_cursor.execute(sql_server_query).fetchall()
    return result


def good_finder_by_id(id):
    sql_server_query = (f"SELECT Zagros_Goods.*,"
                        f"Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن],"
                        f"Zagros_StockGoods.[شناسه کالا]FROM Zagros_Goods JOIN Zagros_StockGoods ON "
                        f"Zagros_Goods.[کد کالا] = Zagros_StockGoods.[کد کالا]WHERE "
                        f"Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن] IS NOT NULL"
                        f" AND [مرکز توزیع] = 'شیراز' AND Zagros_StockGoods.[شناسه کالا] ='{id}'")
    result = sql_server_cursor.execute(sql_server_query).fetchall()
    return result


def create_order(cart_items, customer_id):
    url = "http://vnapishz.zagros-grp.com:9096/api/ThirdPartyOrderAPI/CreateOrder?actiontype=1"
    # ایجاد لیستی از دیکشنری‌ها که معادل orderitems است
    orderitems = []
    for item in cart_items:
        orderitems.append({
            "ReferenceKey": "",
            "ReferenceNo": "",
            "OrderDate": "1402/12/05",
            "StockId": 1,
            "OrderTypeId": 2,
            "CustomerId": customer_id,
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
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJ1c2VybmFtZSI6InZhcmFuZWdhciIsImZ1'
                         'bGxuYW1lIjoi2YjYsdin2Ybar9ixIiwibmJmIjoxNzAzOTE1NDI2LCJleHAiOjE3MDY1MDc0MjYsImlhdCI6MTcwMzkxN'
                         'TQyNiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo0NDM4NSIsImF1ZCI6InRoaXJkcGFydHlVc2VyIn0.djVWn5971u92Hw'
                         'gMZpV9aZ8_AA9y3UE0c9Dnj-GqiaM',
        'AccYear': '1401',
        'CenterId': '3',
        'SaleOfficeId': '1',
        'Language': 'en',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


