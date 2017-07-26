通常在读写文件之前，需要判断文件或目录是否存在，不然某些处理方法可能会使程序出错。所以最好在做任何操作之前，先判断文件是否存在。

这里将介绍三种判断文件或文件夹是否存在的方法，分别使用`os模块`、`Try语句`、`pathlib模块`。

## 1.使用os模块

os模块中的`os.path.exists()`方法用于检验文件是否存在。

* 判断文件是否存在

```python
import os
os.path.exists(test_file.txt)
#True
 
os.path.exists(no_exist_file.txt)
#False
```

* 判断文件夹是否存在

```python
import os
os.path.exists(test_dir)
#True
 
os.path.exists(no_exist_dir)
#False
```

可以看出用`os.path.exists()`方法，判断文件和文件夹是一样。

其实这种方法还是有个问题，假设你想检查文件“test_data”是否存在，但是当前路径下有个叫“test_data”的文件夹，这样就可能出现误判。为了避免这样的情况，可以这样:

* 只检查文件
```
import os
os.path.isfile("test-data")
```

通过这个方法，如果文件"test-data"不存在将返回False，反之返回True。

即是文件存在，你可能还需要判断文件是否可进行读写操作。

## 判断文件是否可做读写操作

使用`os.access()`方法判断文件是否可进行读写操作。

语法：

> os.access(<path>, <mode>)

path为文件路径，mode为操作模式，有这么几种:

* os.F_OK: 检查文件是否存在;

* os.R_OK: 检查文件是否可读;

* os.W_OK: 检查文件是否可以写入;

* os.X_OK: 检查文件是否可以执行

该方法通过判断文件路径是否存在和各种访问模式的权限返回True或者False。

```python
import os
if os.access("/file/path/foo.txt", os.F_OK):
    print "Given file path is exist."
 
if os.access("/file/path/foo.txt", os.R_OK):
    print "File is accessible to read"
 
if os.access("/file/path/foo.txt", os.W_OK):
    print "File is accessible to write"
 
if os.access("/file/path/foo.txt", os.X_OK):
    print "File is accessible to execute"
```

## 2.使用Try语句

可以在程序中直接使用`open()`方法来检查文件是否存在和可读写。

语法：

>open(<file/path>)

如果你open的文件不存在，程序会抛出错误，使用try语句来捕获这个错误。

程序无法访问文件，可能有很多原因：

* 如果你open的文件不存在，将抛出一个`FileNotFoundError`的异常;

* 文件存在，但是没有权限访问，会抛出一个`PersmissionError`的异常。

所以可以使用下面的代码来判断文件是否存在:

```python
try:
    f =open()
    f.close()
except FileNotFoundError:
    print "File is not found."
except PersmissionError:
    print "You don't have permission to access this file."
```

其实没有必要去这么细致的处理每个异常，上面的这两个异常都是`IOError`的子类。所以可以将程序简化一下:

```python
try:
    f =open()
    f.close()
except IOError:
    print "File is not accessible."
```

使用try语句进行判断，处理所有异常非常简单和优雅的。而且相比其他不需要引入其他外部模块。

3. 使用pathlib模块

pathlib模块在Python3版本中是内建模块，但是在Python2中是需要单独安装三方模块。

使用pathlib需要先使用文件路径来创建path对象。此路径可以是文件名或目录路径。

* 检查路径是否存在

```python
path = pathlib.Path("path/file")
path.exist()
```

* 检查路径是否是文件

```python
path = pathlib.Path("path/file")
path.is_file()
```



