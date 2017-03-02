　　re模块提供了一系列功能强大的正则表达式(regular expression)工具，它们允许你快速检查给定字符串是否与给定的模式匹配(match函数), 或者包含这个模式(search函数)。正则表达式是以紧凑(也很神秘)的语法写出的字符串模式。

## 1. 常用方法

|  常用方法 | 描述 |
|---|---|
| match(pattern, string, flags=0) |如果字符串string的开头和正则表达式pattern匹配返回相应的MatchObject的实例，否则返回None|
| search(pattern, string, flags=0) | 扫描string，如果有个位置可以匹配正则表达式pattern，就返回一个MatchObject的实例，否则返回None |
| sub(pattern, repl, string, count=0, flags=0)| 将string里匹配pattern的部分，用repl替换掉，最多替换count次|
| subn(pattern, repl, string, count=0, flags=0)| 和sub类似，subn返回的是一个替换后的字符串和匹配次数组成的元组|
| split(pattern, string, maxsplit=0, flags=0)| 用pattern匹配到的字符串来分割string |
| findall(pattern, string, flags=0) | 以列表的形式返回string里匹配pattern的字符串 |
| compile(pattern, flags=0)compile(pattern, flags=0) | 把一个正则表达式pattern编译成正则对象，以便可以用正则对象的match和search方法 |
| purge()| Clear the regular expression cache |
| escape(string)| 把string中除了字母和数字以外的字符，都加上反斜杆 |

## 2. 特殊匹配符

| 语法  | 说明
|---|---|
| .  | 匹配除了换行符外的任何字符 |
| ^  | 头匹配 |
| $ | 尾匹配 |
| * | 匹配前一个字符0次或多次|
| + | 匹配前一个字符1次或多次|
| ? | 匹配前一个字符0次或一次|

