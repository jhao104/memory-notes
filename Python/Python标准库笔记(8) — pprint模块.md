>pprint —— 更美观的打印数据结构

`pprint` 模块包含一个“美观打印器(`PrettyPrinter`)”，用于产生美观的数据结构视图。格式化程序生成可以由解释器正确解析的数据结构，并且容易使人阅读。

下面所有的例子都将依赖定义在 `pprint_data.py` 中的 `data` 数据结构:

```python
# pprint_data.py

data = [
    (1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
    (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
         'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}),
    (3, ['m', 'n']),
    (4, ['o', 'p', 'q']),
    (5, ['r', 's', 't''u', 'v', 'x', 'y', 'z']),
]
```

### 1.Printing

使用 `pprint` 模块的最简单方法是调用 `pprint()` 方法：

```python
from pprint import pprint

from pprint_data import data

print('PRINT:')
print(data)
print()
print('PPRINT:')
pprint(data)
```

`pprint(object, stream=None, indent=1, width=80, depth=None)` 格式化对象，并将其写入作为参数传入的stream（默认情况下为 `sys.stdout`）。
```python
PRINT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}), (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}), (3, ['m', 'n']), (4, ['o', 'p', 'q']), (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]

PPRINT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]
```

### 2.Formatting

如果仅仅是要格式化数据结构，而不直接将其写stream(例如，如果要写入日志)，则可以使用 `pformat()` 来构建格式化的字符串表示:

```python
import logging
from pprint import pformat
from pprint_data import data

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s %(message)s',
)
logging.debug('Logging pformatted data')

formatted = pformat(data)

for line in formatted.splitlines():
    logging.debug(line.rstrip())
```

`pformat()` 将原数据结构转化为格式化的字符串形式。这里通过logging输出日志。

```python
DEBUG    Logging pformatted data
DEBUG    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
DEBUG     (2,
DEBUG      {'e': 'E',
DEBUG       'f': 'F',
DEBUG       'g': 'G',
DEBUG       'h': 'H',
DEBUG       'i': 'I',
DEBUG       'j': 'J',
DEBUG       'k': 'K',
DEBUG       'l': 'L'}),
DEBUG     (3, ['m', 'n']),
DEBUG     (4, ['o', 'p', 'q']),
DEBUG     (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]
```

### 3. 作用任意类

`pprint` 的“美观打印器(`PrettyPrinter`)”不仅仅支持`list/dict`等,它也支持所有定义了 `__repr__` 方法的任意类。

```python
from pprint import pprint


class Node(object):

    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]

    def __repr__(self):
        return (
            'node(' + repr(self.name) + ', ' +
            repr(self.contents) + ')'
        )


trees = [
    Node('node-1'),
    Node('node-2', [Node('node-2-1')]),
    Node('node-3', [Node('node-3-1')]),
]

pprint(trees)
```

`PrettyPrinter` 会将这些嵌套对象组合起来返回完整的字符串表示。
```python
[node('node-1', []),
 node('node-2', [node('node-2-1', [])]),
 node('node-3', [node('node-3-1', [])])]
```

### 4. 作用递归结构

当作用于递归数据结构时,会以引用原数据来源的方式表示，格式如 `<Recursion on typename with id=number>`， `number`的值是对象的内存地址:

```python
from pprint import pprint

local_data = ['a', 'b', 1, 2]
local_data.append(local_data)

print('id(local_data) =>', id(local_data))
print(local_data)
pprint(local_data)
```

在上面代码中 `local_data` 将它自己添加到自己，变成了一个递归引用。

```python
('id(local_data) =>', 91945672L)
['a', 'b', 1, 2, [...]]
['a', 'b', 1, 2, <Recursion on list with id=91945672>]
```

### 5. 限制嵌套层数

对于非常深的数据结构，可能并不需要输出所有层级细节。数据可能无法正确格式化，格式化的文本也可能因为太大而无法管理，或者可能某些数据是无关的。

使用 ``depth`` 参数来控制 `PrettyPrinter` 递归到嵌套数据结构的深度。输出中不包含的级别由省略号表示：

```python
from pprint import pprint

from pprint_data import data

pprint(data, depth=1)
pprint(data, depth=2)
```

```python
[(...), (...), (...), (...), (...)]
[(1, {...}), (2, {...}), (3, [...]), (4, [...]), (5, [...])]
```

### 6. 控制输出宽度

默认的输出宽度是80个字符长度, 可以使用 `pprint()` 的 ``width`` 参数来调整宽度:

```python
from pprint import pprint

from pprint_data import data

for width in [80, 5]:
    print('WIDTH =', width)
    pprint(data, width=width)
    print()
```

当宽度太小而不能容纳格式化的数据结构时，如果这样做会导致无效的语法，则行不会被截断或包装：
```python
('WIDTH =', 80)
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]

('WIDTH =', 5)
[(1,
  {'a': 'A',
   'b': 'B',
   'c': 'C',
   'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3,
  ['m',
   'n']),
 (4,
  ['o',
   'p',
   'q']),
 (5,
  ['r',
   's',
   'tu',
   'v',
   'x',
   'y',
   'z'])]
```

`pprint()` 的 `compact` 参数表示，在每个单独的行上添加更多的数据，而不是跨行扩展复杂的数据结构（Py2版本无此参数）:

```python
from pprint import pprint

from pprint_data import data

print('DEFAULT:')
pprint(data, compact=False)
print('\nCOMPACT:')
pprint(data, compact=True)
```

```python
DEFAULT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]

COMPACT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']), (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]
```

上面例子表明，设置 `compact` 后, 当数据结构不适合一行时，它就会被拆分(就像 `data` 列表中的第二项一样)。当多个元素可以在一行上时，就像第三个和第四个成员一样，会被放置在一行。