### 简介

图片验证码识别的可以分为几个步骤，一般用 `Pillow` 库或 `OpenCV` 来实现，这几个过程是：
* 1.灰度处理&二值化
* 2.降噪
* 3.字符分割
* 4.标准化
* 5.识别

所谓降噪就是把不需要的信息通通去除，比如背景，干扰线，干扰像素等等，只留下需要识别的字符，让图片变成2进制点阵，方便代入模型训练。

### 8邻域降噪

`8邻域降噪` 的前提是将图片灰度化，即将彩色图像转化为灰度图像。以RGN色彩空间为例，彩色图像中每个像素的颜色由R 、G、B三个分量决定，每个分量由0到255种取值，这个一个像素点可以有一千多万种颜色变化。而灰度则是将三个分量转化成一个，使每个像素点只有0-255种取值，这样可以使后续的图像计算量变得少一些。

![](http://qiniu.spiderpy.cn/19-1-29/1.jpg)

以上面的灰度图片为例，图片越接近白色的点像素越接近255，越接近黑色的点像素越接近0，而且验证码字符肯定是非白色的。对于其中噪点大部分都是孤立的小点的，而且字符都是串联在一起的。`8邻域降噪` 的原理就是依次遍历图中所有非白色的点，计算其周围8个点中属于非白色点的个数，如果数量小于一个固定值，那么这个点就是噪点。对于不同类型的验证码这个阈值是不同的，所以可以在程序中配置，不断尝试找到最佳的阈值。

经过测试`8邻域降噪` 对于小的噪点的去除是很有效的，而且计算量不大，下图是阈值设置为4去噪后的结果：

![](http://qiniu.spiderpy.cn/19-1-29/1.jpg)

### Pillow实现

下面是使用 `Pillow` 模块的实现代码:

```python
from PIL import Image


def noise_remove_pil(image_name, k):
    """
    8邻域降噪
    Args:
        image_name: 图片文件命名
        k: 判断阈值

    Returns:

    """

    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        Args:
            img_obj: img obj
            w: width
            h: height
        Returns:
            count (int)
        """
        count = 0
        width, height = img_obj.size
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj.getpixel((_w_, _h_)) < 230:  # 这里因为是灰度图像，设置小于230为非白色
                    count += 1
        return count

    img = Image.open(image_name)
    # 灰度
    gray_img = img.convert('L')

    w, h = gray_img.size
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img.putpixel((_w, _h), 255)
                continue
            # 计算邻域非白色的个数
            pixel = gray_img.getpixel((_w, _h))
            if pixel == 255:
                continue

            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img.putpixel((_w, _h), 255)
    return gray_img


if __name__ == '__main__':
    image = noise_remove_pil("test.jpg", 4)
    image.show()
```


### OpenCV实现

使用`OpenCV`可以提高计算效率:

```python
import cv2


def noise_remove_cv2(image_name, k):
    """
    8邻域降噪
    Args:
        image_name: 图片文件命名
        k: 判断阈值

    Returns:

    """

    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        Args:
            img_obj: img obj
            w: width
            h: height
        Returns:
            count (int)
        """
        count = 0
        width, height = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_w_, _h_] < 230:  # 二值化的图片设置为255
                    count += 1
        return count

    img = cv2.imread(image_name, 1)
    # 灰度
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray_img.shape
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img[_w, _h] = 255
                continue
            # 计算邻域pixel值小于255的个数
            pixel = gray_img[_w, _h]
            if pixel == 255:
                continue

            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img[_w, _h] = 255

    return gray_img


if __name__ == '__main__':
    image = noise_remove_cv2("test.jpg", 4)
    cv2.imshow('img', image)
    cv2.waitKey(10000)
```