　　PyCharm提供了文件和代码模板功能，可以利用此模板来快捷新建代码或文件。比如在PyCharm中新建一个html文件，新的文件并不是空的，而是会自动填充了一些基础的必备的内容，就像这样:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>
```
　　系统自带的模板内容可能并不是想要的，自己可以修改增加个性化的内容，比如我新建一个名为main.py的Python文件，会自动填充这些内容:

```python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py
   Description :
   Author :       JHao
   date：          2017/4/1
-------------------------------------------------
   Change Activity:
                   2017/4/1:
-------------------------------------------------
"""
__author__ = 'JHao'
```

　　File Name为文件名， Author是登录系统的用户名, 日期为当前系统日期。是不是感觉比默认的空白文件好多了。具体的修改步骤是: 【文件(File)】 --> 【设置(Settings)】如图操作, 在【编辑器(Editor)】中找到【文件和代码模板(File and Code Templates)】，选择你想要设置的文件类型进行编辑即可。
    ![example](https://github.com/jhao104/memory-notes/blob/master/Image/2017060501.png)
　　我的模板是这样的:
```python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ${NAME}
   Description :
   Author :       ${USER}
   date：          ${DATE}
-------------------------------------------------
   Change Activity:
                   ${DATE}:
-------------------------------------------------
"""
__author__ = '${USER}'
```

　　附上模板变量:
```
 ${PROJECT_NAME} - 当前Project名称;

 ${NAME} - 在创建文件的对话框中指定的文件名;

 ${USER} - 当前用户名;

 ${DATE} - 当前系统日期;

 ${TIME} - 当前系统时间;

 ${YEAR} - 年;

 ${MONTH} - 月;

 ${DAY} - 日;

 ${HOUR} - 小时;

 ${MINUTE} - 分钟；

 ${PRODUCT_NAME} - 创建文件的IDE名称;

 ${MONTH_NAME_SHORT} - 英文月份缩写, 如: Jan, Feb, etc;

 ${MONTH_NAME_FULL} - 英文月份全称, 如: January, February, etc；
```