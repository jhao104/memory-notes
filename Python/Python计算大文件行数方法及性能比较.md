如何使用Python快速高效地统计出大文件的总行数, 下面是一些实现方法和性能的比较。

* 1.readline读所有行
使用`readlines`方法读取所有行:
```python
def readline_count(file_name):
    return len(open(file_name).readlines())
```


* 2.依次读取每行
依次读取文件每行内容进行计数:
```python
def simple_count(file_name):
    lines = 0
    for _ in open(file_name):
        lines += 1
    return lines
```

* 3.sum计数
使用`sum`函数计数:
```python
def sum_count(file_name):
    return sum(1 for _ in open(file_name))
```
* 4.enumerate枚举计数:
```python
def enumerate_count(file_name):
    with open(file_name) as f:
        for count, _ in enumerate(f, 1):
            pass
    return count
```

* 5.buff count
每次读取固定大小,然后统计行数:
```python
def buff_count(file_name):
    with open(file_name, 'rb') as f:
        count = 0
        buf_size = 1024 * 1024
        buf = f.read(buf_size)
        while buf:
            count += buf.count(b'\n')
            buf = f.read(buf_size)
        return count
```
* 6.wc count
调用使用`wc`命令计算行:
```python
def wc_count(file_name):
    import subprocess
    out = subprocess.getoutput("wc -l %s" % file_name)
    return int(out.split()[0])
```
* 7.partial count
在buff_count基础上引入`partial`:
```python
def partial_count(file_name):
    from functools import partial
    buffer = 1024 * 1024
    with open(file_name) as f:
        return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))
```
* 8.iter count
在buff_count基础上引入`itertools`模块 :
```python
def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)
```
下面是在我本机 4c8g python3.6的环境下,分别测试100m、500m、1g、10g大小文件运行的时间，单位秒：

| 方法| 100M | 500M | 1G | 10G |
| ------------ | ------------ |
| readline_count | 0.25 | 1.82 | 3.27 | 45.04|
| simple_count | 0.13 | 0.85 | 1.58 | 13.53 |
| sum_count | 0.15 | 0.77 | 1.59 | 14.07 |
| enumerate_count | 0.15 | 0.80 | 1.60 | 13.37|
| buff_count | 0.13 | 0.62 | 1.18 | 10.21 |
| wc_count | 0.09 | 0.53 | 0.99 | 9.47 |
| partial_count | 0.12 | 0.55 | 1.11 | 8.92 |
| iter_count | 0.08 | 0.42 | 0.83 | 8.33 |

