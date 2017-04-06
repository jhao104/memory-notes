# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     datetime.py  
   Description :  datetime模块
   Author :       JHao
   date：          2017/4/6
-------------------------------------------------
   Change Activity:
                   2017/4/6: 
-------------------------------------------------
"""
__author__ = 'JHao'

# region date类
from datetime import date

print 'today():', date.today()  # 返回当前日期对象

print 'fromtimestamp(1491448600):', date.fromtimestamp(1491448600)  # 返回时间戳的日期对象

print 'date.fromordinal(1):', date.fromordinal(1)  # 返回对应公历序数的日期对象

from datetime import date

d = date(2017, 04, 06)

print 'd.year:', d.year  # 返回date对象的年份

print 'd.month:', d.month  # 返回date对象的月份

print 'd.day：', d.day  # 返回date对象的日

print 'd.timetuple():', d.timetuple()  # 返回date对象的struct_time结构

print 'd.toordinal():', d.toordinal()  # 返回公历日期的序数

print 'd.weekday():', d.weekday()  # 返回一星期中的第几天,星期一是0

print 'd.isoweekday():', d.isoweekday()  # 返回一星期中的第几天, 星期一1

print 'd.isocalendar():', d.isocalendar()  # 返回一个元组(年份, 这一年的第几周, 周几)

print 'd.isoformat():', d.isoformat()  # 以ISO 8601格式‘YYYY-MM-DD’返回date的字符串形式

print 'd.ctime():', d.ctime()  # 返回一个表示日期的字符串

print 'd.strftime("%Y-%m-%d"):', d.strftime("%Y-%m-%d")  # 返回指定格式的日期字符串

print 'd.replace(year=2012, month=12) :', d.replace(year=2012, month=12)  # 替换

# endregion

# region time类
from datetime import time

t = time(12, 10, 30, 50)

print 't.hour:', t.hour  # time对象小时数

print 't.minute:', t.minute  # time对象分钟数

print 't.second:', t.second  # time对象秒数

print 't.microsecond:', t.microsecond  # time对象微秒数

print 't.isoformat():', t.isoformat()  # 返回ISO 8601格式的时间字符串

print 't.strftime("%H:%M:%S:%f"):', t.strftime("%H:%M:%S:%f")  # 返回指定格式的时间格式

print 't.replace(hour=23, minute=0):', t.replace(hour=23, minute=0)  # 替换

# endregion

# region datetime类
from datetime import datetime, time, date

print 'datetime.today():', datetime.today()  # 返回本地当前的时间datetime对象

print 'datetime.now():', datetime.now()  # 返回本地当前的日期和时间的datetime对象

print 'datetime.utcnow():', datetime.utcnow()  # 返回当前UTC日期和时间的datetime对象

print 'datetime.fromtimestamp(1491468000):', datetime.fromtimestamp(1491468000)  # 返回对应时间戳的datetime对象

print 'datetime.fromordinal(699000):', datetime.fromordinal(699000)  # 同date.fromordinal类似

print 'datetime.combine(date(2012,12,12), time(12,12,12)):', datetime.combine(date(2012, 12, 12),
                                                                              time(23, 59, 59))  # 拼接date和time

print 'datetime.strptime("2012-12-10", "%Y-%m-%d"):', datetime.strptime("2012-12-10",
                                                                        "%Y-%m-%d")  # 将特定格式的日期时间字符串解析成datetime对象

d = datetime(2017, 04, 06, 12, 10, 30)

print 'd.date():', d.date()  # 从datetime中拆分出date

print 'd.time():', d.time()  # 从datetime中拆分出time

print 'd.timetz()', d.timetz()  # 从datetime中拆分出具体时区属性的time

print 'd.replace(year=2016):', d.replace(year=2016)  # 替换

print 'd.timetuple():', d.timetuple()  # 时间数组,即struct_time结构

print 'd.toordinal():', d.toordinal()  # 和date.toordinal一样

print 'd.weekday():', d.weekday()  # 和date.weekday一样

print 'd.isoweekday():', d.isoweekday()  # 和date.isoweekday一样

print 'd.isocalendar():', d.isocalendar()  # 和date.isocalendar一样

print 'd.isoformat():', d.isoformat()  # 同上

print 'd.ctime():', d.ctime()  # 同上

print 'd.strftime("%Y/%m/%d %H:%M:%S"):', d.strftime('%Y/%m/%d %H:%M:%S')  # 同上
# endregion
