本文简要介绍Python自然语言处理(NLP)，使用Python的NLTK库。NLTK是Python的自然语言处理工具包，在NLP领域中，最常使用的一个Python库。

## 什么是NLP？

简单来说，自然语言处理(NLP)就是开发能够理解人类语言的应用程序或服务。

这里讨论一些自然语言处理(NLP)的实际应用例子，如语音识别、语音翻译、理解完整的句子、理解匹配词的同义词，以及生成语法正确完整句子和段落。

这并不是NLP能做的所有事情。

## NLP实现

**搜索引擎**: 比如谷歌，Yahoo等。谷歌搜索引擎知道你是一个技术人员，所以它显示与技术相关的结果；

**社交网站推送**:比如Facebook News Feed。如果News Feed算法知道你的兴趣是自然语言处理，就会显示相关的广告和帖子。

**语音引擎**:比如Apple的Siri。

**垃圾邮件过滤**:如谷歌垃圾邮件过滤器。和普通垃圾邮件过滤不同，它通过了解邮件内容里面的的深层意义，来判断是不是垃圾邮件。

## NLP库

下面是一些开源的自然语言处理库(NLP)：

* Natural language toolkit (NLTK);
* Apache OpenNLP;
* Stanford NLP suite;
* Gate NLP library

其中自然语言工具包(NLTK)是最受欢迎的自然语言处理库(NLP)，它是用Python编写的，而且背后有非常强大的社区支持。

NLTK也很容易上手，实际上，它是最简单的自然语言处理(NLP)库。

在这个NLP教程中，我们将使用Python NLTK库。

## 安装 NLTK

如果您使用的是Windows/Linux/Mac，您可以使用pip安装NLTK:
```shell
pip install nltk
```

打开python终端导入NLTK检查NLTK是否正确安装：
```python
import mltk
```

如果一切顺利，这意味着您已经成功地安装了NLTK库。首次安装了NLTK，需要通过运行以下代码来安装NLTK扩展包:
```python
import nltk

nltk.download()
```

这将弹出NLTK 下载窗口来选择需要安装哪些包:
![](http://qiniu.spiderpy.cn/17-9-28/34289431.jpg)

您可以安装所有的包，因为它们的大小都很小，所以没有什么问题。

## 使用Python Tokenize文本

首先，我们将抓取一个web页面内容，然后分析文本了解页面的内容。

我们将使用urllib模块来抓取web页面:
```python
import urllib.request

response = urllib.request.urlopen('http://php.net/')
html = response.read()
print (html)
```

从打印结果中可以看到，结果包含许多需要清理的HTML标签。
然后BeautifulSoup模块来清洗这样的文字:
```python
from bs4 import BeautifulSoup

import urllib.request
response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
# 这需要安装html5lib模块
text = soup.get_text(strip=True)
print (text)
```

现在我们从抓取的网页中得到了一个干净的文本。
下一步，将文本转换为tokens,像这样:
```python
from bs4 import BeautifulSoup
import urllib.request

response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
text = soup.get_text(strip=True)
tokens = [t for t in text.split()]
print (tokens)
```

## 统计词频
text已经处理完毕了，现在使用Python NLTK统计token的频率分布。

可以通过调用NLTK中的`FreqDist()`方法实现:
```python
from bs4 import BeautifulSoup
import urllib.request
import nltk

response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
text = soup.get_text(strip=True)
tokens = [t for t in text.split()]
freq = nltk.FreqDist(tokens)
for key,val in freq.items():
    print (str(key) + ':' + str(val))
```

如果搜索输出结果，可以发现最常见的token是PHP。
您可以调用`plot`函数做出频率分布图:
```python
freq.plot(20, cumulative=False)
# 需要安装matplotlib库
```
![](http://qiniu.spiderpy.cn/17-9-28/51431526.jpg)

这上面这些单词。比如`of`,`a`,`an`等等，这些词都属于停用词。

一般来说，停用词应该删除，防止它们影响分析结果。

## 处理停用词

NLTK自带了许多种语言的停用词列表，如果你获取英文停用词:
```python
from nltk.corpus import stopwords

stopwords.words('english')
```

现在，修改下代码,在绘图之前清除一些无效的token:
```python
clean_tokens = list()
sr = stopwords.words('english')
for token in tokens:
    if token not in sr:
        clean_tokens.append(token)
```

最终的代码应该是这样的:
```python
from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.corpus import stopwords

response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
text = soup.get_text(strip=True)
tokens = [t for t in text.split()]
clean_tokens = list()
sr = stopwords.words('english')
for token in tokens:
    if not token in sr:
        clean_tokens.append(token)
freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items():
    print (str(key) + ':' + str(val))
```
现在再做一次词频统计图，效果会比之前好些，因为剔除了停用词:
```python
freq.plot(20,cumulative=False)
```

![](http://qiniu.spiderpy.cn/17-9-28/50754369.jpg)

## 使用NLTK Tokenize文本

在之前我们用`split`方法将文本分割成tokens，现在我们使用NLTK来Tokenize文本。

文本没有Tokenize之前是无法处理的，所以对文本进行Tokenize非常重要的。token化过程意味着将大的部件分割为小部件。

你可以将段落tokenize成句子，将句子tokenize成单个词，NLTK分别提供了句子tokenizer和单词tokenizer。

假如有这样这段文本:
```markdown
Hello Adam, how are you? I hope everything is going well. Today is a good day, see you dude.
```

使用句子tokenizer将文本tokenize成句子:
```python
from nltk.tokenize import sent_tokenize

mytext = "Hello Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
print(sent_tokenize(mytext))
```

输出如下:
```python
['Hello Adam, how are you?', 'I hope everything is going well.', 'Today is a good day, see you dude.']
```

这是你可能会想，这也太简单了，不需要使用NLTK的tokenizer都可以，直接使用正则表达式来拆分句子就行，因为每个句子都有标点和空格。

那么再来看下面的文本:
```python
Hello Mr. Adam, how are you? I hope everything is going well. Today is a good day, see you dude.
```

这样如果使用标点符号拆分,`Hello Mr`将会被认为是一个句子，如果使用NLTK:
```python
from nltk.tokenize import sent_tokenize

mytext = "Hello Mr. Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
print(sent_tokenize(mytext))
```

输出如下:
```python
['Hello Mr. Adam, how are you?', 'I hope everything is going well.', 'Today is a good day, see you dude.']
```

这才是正确的拆分。

接下来试试单词tokenizer:
```python
from nltk.tokenize import word_tokenize

mytext = "Hello Mr. Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
print(word_tokenize(mytext))
```

输出如下:
```python
['Hello', 'Mr.', 'Adam', ',', 'how', 'are', 'you', '?', 'I', 'hope', 'everything', 'is', 'going', 'well', '.', 'Today', 'is', 'a', 'good', 'day', ',', 'see', 'you', 'dude', '.']
```

`Mr.`这个词也没有被分开。NLTK使用的是punkt模块的PunktSentenceTokenizer，它是NLTK.tokenize的一部分。而且这个tokenizer经过训练，可以适用于多种语言。

## 非英文Tokenize

Tokenize时可以指定语言:
```python
from nltk.tokenize import sent_tokenize

mytext = "Bonjour M. Adam, comment allez-vous? J'espère que tout va bien. Aujourd'hui est un bon jour."
print(sent_tokenize(mytext,"french"))
```

输出结果如下:
```python
['Bonjour M. Adam, comment allez-vous?', "J'espère que tout va bien.", "Aujourd'hui est un bon jour."]
```

## 同义词处理

使用`nltk.download()`安装界面，其中一个包是WordNet。

WordNet是一个为自然语言处理而建立的数据库。它包括一些同义词组和一些简短的定义。

您可以这样获取某个给定单词的定义和示例:
```python
from nltk.corpus import wordnet

syn = wordnet.synsets("pain")
print(syn[0].definition())
print(syn[0].examples())
```

输出结果是:
```python
a symptom of some physical hurt or disorder
['the patient developed severe pain and distension']
```

WordNet包含了很多定义：
```python
from nltk.corpus import wordnet

syn = wordnet.synsets("NLP")
print(syn[0].definition())
syn = wordnet.synsets("Python")
print(syn[0].definition())
```

结果如下:
```python
the branch of information science that deals with natural language information
large Old World boas
```

可以像这样使用WordNet来获取同义词:
```python
from nltk.corpus import wordnet

synonyms = []
for syn in wordnet.synsets('Computer'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
print(synonyms)
```

输出:
```python
['computer', 'computing_machine', 'computing_device', 'data_processor', 'electronic_computer', 'information_processing_system', 'calculator', 'reckoner', 'figurer', 'estimator', 'computer']
```

## 反义词处理

也可以用同样的方法得到反义词：
```python
from nltk.corpus import wordnet

antonyms = []
for syn in wordnet.synsets("small"):
    for l in syn.lemmas():
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(antonyms)
```

输出:
```python
['large', 'big', 'big']
```

## 词干提取

语言形态学和信息检索里，词干提取是去除词缀得到词根的过程，例如working的词干为work。

搜索引擎在索引页面时就会使用这种技术，所以很多人为相同的单词写出不同的版本。

有很多种算法可以避免这种情况，最常见的是**波特词干算法**。NLTK有一个名为PorterStemmer的类，就是这个算法的实现:
```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
print(stemmer.stem('working'))
print(stemmer.stem('worked'))
```

输出结果是:
```python
work
work
```

还有其他的一些词干提取算法，比如 **Lancaster词干算法**。

## 非英文词干提取

除了英文之外，SnowballStemmer还支持13种语言。

支持的语言:
```python
from nltk.stem import SnowballStemmer

print(SnowballStemmer.languages)
```
```python
'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish'
```

你可以使用`SnowballStemmer`类的`stem`函数来提取像这样的非英文单词：
```python
from nltk.stem import SnowballStemmer

french_stemmer = SnowballStemmer('french')

print(french_stemmer.stem("French word"))
```

## 单词变体还原

单词变体还原类似于词干，但不同的是，变体还原的结果是一个真实的单词。不同于词干，当你试图提取某些词时，它会产生类似的词:
```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

print(stemmer.stem('increases'))
```

结果:
```python
increas
```

现在，如果用NLTK的WordNet来对同一个单词进行变体还原，才是正确的结果:
```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize('increases'))
```

结果:
```python
increase
```

结果可能会是一个同义词或同一个意思的不同单词。

有时候将一个单词做变体还原时，总是得到相同的词。

这是因为语言的默认部分是名词。要得到动词，可以这样指定：
```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize('playing', pos="v"))
```

结果:
```python
play
```

实际上，这也是一种很好的文本压缩方式，最终得到文本只有原先的50%到60%。

结果还可以是动词(v)、名词(n)、形容词(a)或副词(r)：
```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('playing', pos="v"))
print(lemmatizer.lemmatize('playing', pos="n"))
print(lemmatizer.lemmatize('playing', pos="a"))
print(lemmatizer.lemmatize('playing', pos="r"))
```

输出:
```python
play
playing
playing
playing
```

## 词干和变体的区别

通过下面例子来观察:
```python
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
print(stemmer.stem('stones'))
print(stemmer.stem('speaking'))
print(stemmer.stem('bedroom'))
print(stemmer.stem('jokes'))
print(stemmer.stem('lisa'))
print(stemmer.stem('purple'))
print('----------------------')
print(lemmatizer.lemmatize('stones'))
print(lemmatizer.lemmatize('speaking'))
print(lemmatizer.lemmatize('bedroom'))
print(lemmatizer.lemmatize('jokes'))
print(lemmatizer.lemmatize('lisa'))
print(lemmatizer.lemmatize('purple'))
```

输出:
```python
stone
speak
bedroom
joke
lisa
purpl
---------------------
stone
speaking
bedroom
joke
lisa
purple
```

词干提取不会考虑语境，这也是为什么词干提取比变体还原快且准确度低的原因。

个人认为，变体还原比词干提取更好。单词变体还原返回一个真实的单词，即使它不是同一个单词，也是同义词，但至少它是一个真实存在的单词。

如果你只关心速度，不在意准确度，这时你可以选用词干提取。

在此NLP教程中讨论的所有步骤都只是文本预处理。在以后的文章中，将会使用Python NLTK来实现文本分析。

我已经尽量使文章通俗易懂。希望能对你有所帮助。