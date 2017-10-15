captcha模块是专门用于生成图形验证码和语音验证码的Python三方库。图形验证码支持数字和英文单词。

## 安装

### 安装
可以直接使用 `pip` 安装，或者到[项目地址](https://github.com/lepture/captcha)下载安装。

### 模块支持

由于 `captcha` 模块内部是采用 `PIL` 模块生成图片，所以需要安装 `PIL` 模块才可以正常使用。


## 生成验证码

### 一般方法

使用其中 `image` 模块中的 `ImageCaptcha` 类生成图形验证码：

```python
from captcha.image import ImageCaptcha

img = ImageCaptcha()
image = img.generate_image('python')
image.show()
image.save('python.jpg')
```

生成验证码如下:

![captcha1](http://qiniu.spiderpy.cn/17-10-15/29089691.jpg)

`generate_image（）` 方法接收一个字符串参数，将生成次字符串内容的验证码，返回的是 `PIL` 模块中的 `Image` 对象。可以使用 `PIL` 模块中 `Image` 对象的任何支持方法对其操作。例子中的 `image.show()` 和 `image.save()` 均是 `PIL` 模块的方法。

### 具体参数

`ImageCaptcha(width=160, height=60, fonts=None, font_sizes=None)` 类实例化时，还可传入四个参数:

* `width`: 生成验证码图片的宽度，默认为160个像素；
* `height`： 生成验证码图片的高度，默认为60个像素；
* `fonts`： 字体文件路径，用于生成验证码时的字体，默认使用模块自带 `DroidSansMono.ttf` 字体，你可以将字体文件放入list或者tuple传入,生成验证码时将随机使用;
* `font_sizes`： 控制验证码字体大小，同`fonts`一样，接收一个list或者tuple,随机使用。

### 主要方法

* `generate_image(chars)`
生成验证码的核心方法，生成`chars`内容的验证码图片的`Image`对象。

* `create_captcha_image(chars, color, background)`
`generate_image`的实现方法，可以通过重写此方法来实现自定义验证码样式。

* `create_noise_dots(image, color, width=3, number=30)`
生成验证码干扰点。

* `create_noise_curve(image, color)`
生成验证码干扰曲线




