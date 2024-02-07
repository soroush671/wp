import requests
import datetime

print(datetime.datetime.now())
url = "http://vnapishz.zagros-grp.com:9096/ThirdPartyStockProductInfoOData?skip=1000"

payload = {}
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJ1c2VybmFtZSI6InZhcmFuZWdhciIsImZ1bGxuYW1'
                   'lIjoi2YjYsdin2Ybar9ixIiwibmJmIjoxNzAzOTE1NDI2LCJleHAiOjE3MDY1MDc0MjYsImlhdCI6MTcwMzkxNTQyNiwiaXNzIj'
                   'oiaHR0cDovL2xvY2FsaG9zdDo0NDM4NSIsImF1ZCI6InRoaXJkcGFydHlVc2VyIn0.djVWn5971u92HwgMZpV9aZ8_AA9y3UE0c'
                   '9Dnj-GqiaM',
  'AccYear': '1401',
  'CenterId': '3',
  'SaleOfficeId': '1',
  'Language': 'en'
}
all_data = []

while url:
    response = requests.get(url)
    data = response.json()

    # اضافه کردن داده‌های صفحه فعلی به لیست
    all_data.extend(data.get('value', []))

    # دریافت لینک بعدی در صورت وجود
    url = data.get('@odata.nextLink')

# حالا متغیر all_data شامل تمام اطلاعات است
# print(all_data)
for product in all_data:
    print(f"Product Name: {product.get('GoodsName')}")
    print(f"Product Code: {product.get('GoodsCode')}")
    print(f"Sale Price: {product.get('SalePrice')}")
    print("\n")

print(datetime.datetime.now())
print(all_data)