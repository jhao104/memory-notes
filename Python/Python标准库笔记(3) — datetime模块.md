> datetime模块提供了简单和复杂的方式用于操纵日期和时间的类。虽然支持日期和时间运算，但实现的重点是为了输出格式化和操作高效地提取属性。

## 1. 模块内容

| 内容  | 描述 |
|---| --- |
| 常量  || 
| datetime.MINYEAR | date和datetime对象允许的最小年份|
| datetime.MAXYEAR | date和datetime对象允许的最大年份|
| 类 ||
| datetime.date | 日期对象,属性(year, month, day) |
| datetime.time | 时间对象,属性(hour, minute, second, microsecond, tzinfo)|  
| datetime.datetime | 日期时间对象,属性(date和time属性组合)|
| datetime.timedelta |  Difference between two datetime values(原文)|
| datetime.tzinfo | 时区信息对象的抽象基类, datetime和time类使用它定制化时间调节 |

## 2. datetime.date类
　　date对象表示理想化日历中的日期(年、月和日), 公历1年1月1日被称为第一天，依次往后推。

* 类方法

```python
from datetime import date

print 'today():', date.today()  # 返回当前日期对象

print 'fromtimestamp(1491448600):', date.fromtimestamp(1491448600)  # 返回时间戳的日期对象

print 'date.fromordinal(1):', date.fromordinal(1)  # 返回对应公历序数的日期对象

# 输出
today():2017-04-06
fromtimestamp(1491448600):2017-04-06
date.fromordinal(1): 0001-01-01
```

* 对象方法和属性

```python
from datetime import date

d = date(2017, 04, 06)

print 'd.year:', d.year    # 返回date对象的年份

print 'd.month:', d.month  # 返回date对象的月份

print 'd.day：', d.day     # 返回date对象的日

print 'd.timetuple():', d.timetuple()  # 返回date对象的struct_time结构

print 'd.toordinal():', d.toordinal()  # 返回公历日期的序数

print 'd.weekday():', d.weekday()      # 返回一星期中的第几天,星期一是0

print 'd.isoweekday():', d.isoweekday()  # 返回一星期中的第几天, 星期一1

print 'd.isocalendar():', d.isocalendar()  # 返回一个元组(年份, 这一年的第几周, 周几)

print 'd.isoformat():', d.isoformat()  # 以ISO 8601格式‘YYYY-MM-DD’返回date的字符串形式

print 'd.ctime():', d.ctime()  # 返回一个表示日期的字符串

print 'd.strftime("%Y-%m-%d"):', d.strftime("%Y-%m-%d")  # 返回指定格式的日期字符串

print 'd.replace(year=2012, month=12) :', d.replace(year=2012, month=12)  # 替换



# 输出

d.year: 2017
d.month: 4
d.day： 6
d.timetuple(): time.struct_time(tm_year=2017, tm_mon=4, tm_mday=6, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=96, tm_isdst=-1)
d.toordinal(): 736425
d.weekday(): 3
d.isoweekday(): 4
d.isocalendar(): (2017, 14, 4)
d.isoformat(): 2017-04-06
d.ctime(): Thu Apr  6 00:00:00 2017
d.strftime("%Y-%m-%d"): 2017-04-06
d.replace(year=2012, month=12) : 2012-12-06
```

## 3. datetime.time类

　　表示一个(当地)时间对象，与任何特定的日期无关，并且可以通过tzinfo(时区)对象进行调整。

```python
from datetime import time

t = time(12, 10, 30, 50)

print 't.hour:', t.hour      # time对象小时数

print 't.minute:', t.minute  # time对象分钟数

print 't.second:', t.second  # time对象秒数

print 't.microsecond:', t.microsecond  # time对象微秒数

print 't.isoformat():', t.isoformat()  # 返回ISO 8601格式的时间字符串

print 't.strftime("%H:%M:%S:%f"):', t.strftime("%H:%M:%S:%f")  # 返回指定格式的时间格式

print 't.replace(hour=23, minute=0):', t.replace(hour=23, minute=0)  # 替换

# 输出

t.hour: 12
t.minute: 10
t.second: 30
t.microsecond: 50
t.isoformat(): 12:10:30.000050
t.strftime("%H:%M:%S:%f"): 12:10:30:000050
t.replace(hour=23, minute=0): 23:00:30.000050
```

## 4. datetime.datetime类

　　datetime对象包含date对象和time对象的所有信息

* 类方法

```python
from datetime import datetime, time, date

print 'datetime.today():', datetime.today()  # 返回本地当前的时间datetime对象

print 'datetime.now():', datetime.now()  # 返回本地当前的日期和时间的datetime对象

print 'datetime.utcnow():', datetime.utcnow()  # 返回当前UTC日期和时间的datetime对象

print 'datetime.fromtimestamp(1491468000):', datetime.fromtimestamp(1491468000)  # 返回对应时间戳的datetime对象

print 'datetime.fromordinal(699000):', datetime.fromordinal(699000)  # 同date.fromordinal类似

print 'datetime.combine(date(2012,12,12), time(12,12,12)):', datetime.combine(date(2012, 12, 12), time(23, 59, 59))  # 拼接date和time

print 'datetime.strptime("2012-12-10", "%Y-%m-%d"):', datetime.strptime("2012-12-10", "%Y-%m-%d")  # 将特定格式的日期时间字符串解析成datetime对象

# 输出
datetime.today(): 2017-04-06 16:53:12.080000
datetime.now(): 2017-04-06 16:53:12.080000
datetime.utcnow(): 2017-04-06 08:53:12.080000
datetime.fromtimestamp(1491468000): 2017-04-06 16:40:00
datetime.fromordinal(699000): 1914-10-19 00:00:00
datetime.combine(date(2012,12,12), time(12,12,12)): 2012-12-12 23:59:59
datetime.strptime("2012-12-10", "%Y-%m-%d"): 2012-12-10 00:00:00
```

* 对象方法和属性

```python
from datetime import datetime
d = datetime(2017, 04, 06, 12, 10, 30)

print 'd.date():', d.date()  # 从datetime中拆分出date

print 'd.time():', d.time()  # 从datetime中拆分出time

print 'd.timetz()', d.timetz()  # 从datetime中拆分出具体时区属性的time

print 'd.replace(year=2016):', d.replace(year=2016)  # 替换

print 'd.timetuple():', d.timetuple()  # 时间数组,即struct_time结构

print 'd.toordinal():', d.toordinal()  # 和date.toordinal一样

print 'd.weekday():', d.weekday()      # 和date.weekday一样

print 'd.isoweekday():', d.isoweekday()  # 和date.isoweekday一样

print 'd.isocalendar():', d.isocalendar()  # 和date.isocalendar一样

print 'd.isoformat():', d.isoformat()  # 同上

print 'd.ctime():', d.ctime()  # 同上

print 'd.strftime("%Y/%m/%d %H:%M:%S"):', d.strftime('%Y/%m/%d %H:%M:%S')  # 同上

# 输出
d.date(): 2017-04-06
d.time(): 12:10:30
d.timetz() 12:10:30
d.replace(year=2016): 2016-04-06 12:10:30
d.timetuple(): time.struct_time(tm_year=2017, tm_mon=4, tm_mday=6, tm_hour=12, tm_min=10, tm_sec=30, tm_wday=3, tm_yday=96, tm_isdst=-1)
d.toordinal(): 736425
d.weekday(): 3
d.isoweekday(): 4
d.isocalendar(): (2017, 14, 4)
d.isoformat(): 2017-04-06T12:10:30
d.ctime(): Thu Apr  6 12:10:30 2017
d.strftime("%Y/%m/%d %H:%M:%S"): 2017/04/06 12:10:30
```

## 5. datetime.timedelta类

　　timedelta对象表示一个时间段，即两个日期 (date) 或日期时间 (datetime) 之间的差。支持参数:weeks、days、hours、minutes、seconds、milliseconds、microseconds。但是据官方文档说其内部只存储days、seconds 和 microseconds,其他单位会做对应的时间转换。


```shell
>>>from datetime import timedelta, date, datetime
>>>d = date.today()
>>>print d
2017-04-06
>>>print d - timedelta(days=5)  # 计算前5天
2017-04-01

>>>dt = datetime.now()
>>>print dt
2017-04-06 17:51:03.568000
>>>print dt - timedelta(days=1, hours=5)  # 计算前1天5小时
2017-04-05 12:51:03.568000
```

## 6. 格式字符串
　　datetime、date、time 都提供了 strftime() 方法，该方法接收一个格式字符串，输出日期时间的字符串表示。支持的转换格式如下：

| 字符  |　含义　|　例子　|
|---|---|---|
| %a  | 英文星期的简写| Sun, Mon, ..., Sat |
| %A |英文星期的全拼 | Sunday, Monday, ..., Saturday |
| %w |星期几,星期天为0,星期六为6| 0, 1, ..., 6 |
| %d | 这个月的第几天,以0填充的10进制|01, 02, ..., 31|
| %b | 月份英文简写| Jan, Feb, ..., Dec|
| %B | 月份英文全拼| January, February, ..., December|
| %m | 月份数，以0填充的10进制|01, 02, ..., 12|
| %y | 不带世纪的年份| 00, 01, ..., 99|
| %Y | 带有世纪的年份| 1970, 1988, 2001, 2013|
| %H | 24小时制的小时数| 00, 01, ..., 23|
| %I | 12小时制的小时数|01, 02, ..., 12|

