from app import sql_server_cursor
from app.models import User, Brand


def user_finder(user_id):
    sql_server_query = f"SELECT * FROM Zagros_Customer WHERE [کد مشتری]='{user_id}'"
    result = sql_server_cursor.execute(sql_server_query).fetchall()
    if result:
        user_data = result[0]  # گرفتن اولین رکورد از نتیجه
        mobile_number = user_data[5]  # فرضاً موبایل در ستون ششم قرار دارد
        user_id = user_data[0]
        shop_name = user_data[2]

        return User(username=user_id, password=mobile_number, shop_name=shop_name)
    else:
        return None


def brand_finder():
    brand = Brand.query.all()
    return brand


def good_list_finder():
    pass
