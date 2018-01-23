该模块作用是完成Python数值和C语言结构体的Python字符串形式间的转换。这可以用于处理存储在文件中或从网络连接中存储的二进制数据，以及其他数据源。

>用途: 在Python基本数据类型和二进制数据之间进行转换

`struct`模块提供了用于在字节字符串和Python原生数据类型之间转换函数，比如数字和字符串。

### 模块函数和Struct类
它除了提供一个`Struct`类之外，还有许多模块级的函数用于处理结构化的值。这里有个格式符(Format specifiers)的概念，是指从字符串格式转换为已编译的表示形式，类似于正则表达式的处理方式。通常实例化`Struct`类，调用类方法来完成转换，比直接调用模块函数有效的多。下面的例子都是使用`Struct`类。

### Packing（打包）和Unpacking（解包）

`Struct`支持将数据packing(打包)成字符串，并能从字符串中逆向unpacking(解压)出数据。

在本例中，格式指定器(specifier)需要一个整型或长整型，一个两个字节的string,和一个浮点数。格式符中的空格用于分隔各个指示器(indicators)，在编译格式时会被忽略。

```python
import struct

import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
s = struct.Struct('I 2s f')
packed_data = s.pack(*values)

print('原始值:', values)
print('格式符:', s.format)
print('占用字节:', s.size)
print('打包结果:', binascii.hexlify(packed_data))
```
```bash
# output
原始值: (1, b'ab', 2.7)
格式符: b'I 2s f'
占用字节: 12
打包结果: b'0100000061620000cdcc2c40'
```

这个示例将打包的值转换为十六进制字节序列，用`binascii.hexlify()`方法打印出来。

使用`unpack()`方法解包。

```python
import struct
import binascii

packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print('解包结果:', unpacked_data)
```
```bash
# output
解包结果: (1, b'ab', 2.700000047683716)
```

将打包的值传给`unpack()`，基本上返回相同的值(浮点数会有差异)。

### 字节顺序/大小/对齐

默认情况下，pack是使用本地C库的字节顺序来编码的。格式化字符串的第一个字符可以用来表示填充数据的字节顺序、大小和对齐方式，如下表所描述的:

|  Character | Byte order  | Size | Alignment  |
| ------------ | ------------ | ------------ | ------------ |
| `@` | 本地 | 本地 | 本地 |
| `=` | 本地 | standard | none |
| `<` | little-endian（小字节序）  | standard | none |
| `>` | big-endian（大字节序） | standard | none |
| `!` | network (= big-endian) | standard | none |

如果格式符中没有设置这些，那么默认将使用 `@`。

本地字节顺序是指字节顺序是由当前主机系统决定。比如：Intel x86和AMD64(x86-64)使用小字节序； Motorola 68000和 PowerPC G5使用大字节序。ARM和Intel安腾支持切换字节序。可以使用`sys.byteorder`查看当前系统的字节顺序。

本地大小(Size)和对齐(Alignment)是由c编译器的`sizeof`表达式确定的。它与本地字节顺序对应。

标准大小由格式符确定，下面会讲各个格式的标准大小。

示例:
```python
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
print('原始值  : ', values)

endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print()
    print('格式符  : ', s.format, 'for', name)
    print('占用字节: ', s.size)
    print('打包结果: ', binascii.hexlify(packed_data))
    print('解包结果: ', s.unpack(packed_data))
```

```python
# output
原始值  :  (1, b'ab', 2.7)

格式符  :  b'@ I 2s f' for native, native
占用字节:  12
打包结果:  b'0100000061620000cdcc2c40'
解包结果:  (1, b'ab', 2.700000047683716)

格式符  :  b'= I 2s f' for native, standard
占用字节:  10
打包结果:  b'010000006162cdcc2c40'
解包结果:  (1, b'ab', 2.700000047683716)

格式符  :  b'< I 2s f' for little-endian
占用字节:  10
打包结果:  b'010000006162cdcc2c40'
解包结果:  (1, b'ab', 2.700000047683716)

格式符  :  b'> I 2s f' for big-endian
占用字节:  10
打包结果:  b'000000016162402ccccd'
解包结果:  (1, b'ab', 2.700000047683716)

格式符  :  b'! I 2s f' for network
占用字节:  10
打包结果:  b'000000016162402ccccd'
解包结果:  (1, b'ab', 2.700000047683716)
```

### 格式符

格式符对照表如下:

| Format | C Type | Python type | Standard size | Notes |
| --- | --- | --- | --- | --- |
| `x` | pad byte | no value | | |
| `c` | `char` | bytes of length 1 | 1 | |
| `b` | `signed char` | integer | 1 | (1),(3) |
| `B` | `unsigned char` | integer | 1 | (3) |
| `?` | `_Bool` | bool | 1 | (1) |
| `h` | `short` | integer | 2 | (3) |
| `H` | `unsigned short` | integer | 2 | (3) |
| `i` | `int` | integer | 4 | (3) |
| `I` | `unsigned int` | integer | 4 | (3) |
| `l` | `long` | integer | 4 | (3) |
| `L` | `unsigned long` | integer | 4 | (3) |
| `q` | `long long` | integer | 8 | (2), (3) |
| `Q` | `unsigned long long` | integer | 8 | (2), (3) |
| `n` | `ssize_t` | integer | (4) | |
| `N` | `size_t` | integer | (4) | |
| `f` | `float` | float | 4 | (5) |
| `d` | `double` | float | 8 | (5) |
| `s` | `char[]` | bytes | | |
| `p` | `char[]` | bytes | | |
| `P` | `void *` | integer | | (6) |

### 缓冲区

将数据打包成二进制通常是用在对性能要求很高的场景。
在这类场景中可以通过避免为每个打包结构分配新缓冲区的开销来优化。
`pack_into()`和`unpack_from()`方法支持直接写入预先分配的缓冲区。

```python
import array
import binascii
import ctypes
import struct

s = struct.Struct('I 2s f')
values = (1, 'ab'.encode('utf-8'), 2.7)
print('原始值:', values)

print()
print('使用ctypes模块string buffer')

b = ctypes.create_string_buffer(s.size)
print('原始buffer  :', binascii.hexlify(b.raw))
s.pack_into(b, 0, *values)
print('打包结果写入 :', binascii.hexlify(b.raw))
print('解包        :', s.unpack_from(b, 0))

print()
print('使用array模块')

a = array.array('b', b'\0' * s.size)
print('原始值   :', binascii.hexlify(a))
s.pack_into(a, 0, *values)
print('打包写入 :', binascii.hexlify(a))
print('解包     :', s.unpack_from(a, 0))
```

```python
# output
原始值: (1, b'ab', 2.7)

使用ctypes模块string buffer
原始buffer  : b'000000000000000000000000'
打包结果写入 : b'0100000061620000cdcc2c40'
解包        : (1, b'ab', 2.700000047683716)

使用array模块
原始值   : b'000000000000000000000000'
打包写入 : b'0100000061620000cdcc2c40'
解包     : (1, b'ab', 2.700000047683716)
```
