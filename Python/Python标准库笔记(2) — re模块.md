　　re模块提供了一系列功能强大的正则表达式(regular expression)工具，它们允许你快速检查给定字符串是否与给定的模式匹配(match函数), 或者包含这个模式(search函数)。正则表达式是以紧凑(也很神秘)的语法写出的字符串模式。

## 1. 常用方法

|  常用方法 | 描述 |
|---|---|
| re.match() |  返回匹配的MatchObject实例或者None |
| re.search() | 扫描字符串，搜索首次由该正则表达式模式产生匹配的位置，并返回相应的MatchObject实例或者None |
| re.sub()| 