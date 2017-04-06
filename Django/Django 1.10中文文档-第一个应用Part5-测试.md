　　本教程上接教程[Part4](https://github.com/jhao104/memory-notes/blob/master/Django/Django%201.10%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3-%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8Part4-%E8%A1%A8%E5%8D%95%E5%92%8C%E9%80%9A%E7%94%A8%E8%A7%86%E5%9B%BE.md)。 前面已经建立一个网页投票应用，现在将为它创建一些自动化测试。

## 什么是自动化测试

　　测试是检查你的代码是否正常运行的行为。测试也分为不同的级别。有些测试可能是用于某个细节操作（比如特定的模型方法是否返回预期的值），而有些测试是检查软件的整体操作（比如站点上的一系列用户输入是否产生所需的结果）。这和[Part2](https://github.com/jhao104/memory-notes/blob/master/Django/Django%201.10%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3-%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8Part2-%E6%A8%A1%E5%9E%8B%E5%92%8C%E7%AE%A1%E7%90%86%E7%AB%99%E7%82%B9.md)中的测试是一样的，使用shell来检查方法的行为，或者运行应用程序并输入数据来检查它的行为。
