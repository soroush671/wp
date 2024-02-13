from app import sql_server_cursor
from app.models import User, Brand

def good_list_finder():
    sql_server_query =("SELECT Zagros_Goods.*,"
                       " Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن]"
                       "FROM Zagros_Goods"
                       " JOIN Zagros_StockGoods ON Zagros_Goods.[کد کالا] = Zagros_StockGoods.[کد کالا]"
                       " WHERE Zagros_StockGoods.[موجودی قابل سفارش با کسر درخواست های صادر نشده - کارتن] "
                       "IS NOT NULL AND [مرکز توزیع]='شیراز'")
    result = sql_server_cursor.execute(sql_server_query).fetchall()
    return result
