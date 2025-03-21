import math
def makeThumbnail(image_path, output_path, max_width, max_height):
    '''
    生成缩略图
    '''
    # 读取原始图片
    from PIL import Image, ImageChops
    img = Image.open(image_path)

    # 计算缩略图的宽度和高度，保持原始图片的比例
    ratio = min(max_width / img.width, max_height / img.height)
    width = int(img.width * ratio)
    height = int(img.height * ratio)

    # 生成缩略图，并保存到文件
    img.thumbnail((width, height), Image.ANTIALIAS)
    img.save(output_path)


def colorOverlay(img, rgba):
    """
    给图像添加颜色叠加层。

    参数:
        img (PIL.Image.Image): 原始图像。
        rgba (tuple): 包含颜色信息的元组，形如 (R, G, B, A)。

    返回:
        PIL.Image.Image: 添加颜色叠加层后的图像。
    """

    # 创建一个与原始图像大小相同的图像，填充指定颜色
    from PIL import Image, ImageChops
    overlay = Image.new("RGBA", img.size, rgba)

    result_image = Image.composite(overlay, Image.new("RGBA", img.size), img.convert("RGBA"))
    return result_image


def setAlpha(img, alpha):
    """
    设置图像的透明度。

    参数:
        img (PIL.Image.Image): 要设置透明度的图像。
        alpha (float): 透明度值，取值范围在 0 到 1 之间。

    返回:
        None: 该函数直接修改传入的图像对象，不返回新的图像。
    """

    alpha1 = img.getchannel("A")
    alpha1 = alpha1.point(lambda x: x * alpha)
    img.putalpha(alpha1)



def removeDarkWithTransparent(input_image_path, output_image_path):
    from PIL import Image
    import colorsys
    # 定义饱和度和明度接近黑色的阈值，可根据实际情况调整
    saturation_threshold = 0.8
    value_threshold = 0.8

    # 打开图片
    image = Image.open(input_image_path)

    # 将图片转换为RGBA模式，以便处理透明度
    image = image.convert("RGBA")

    # 获取图片的像素数据
    data = image.getdata()

    new_data = []
    for item in data:
        # 将RGB颜色转换为HSV颜色空间
        # 色调（Hue）、饱和度（Saturation）和明度（Value）
        hsv = colorsys.rgb_to_hsv(item[0] / 255, item[1] / 255, item[2] / 255)

        # 判断是否接近黑色（饱和度和明度都小于阈值）
        if hsv[1] < saturation_threshold and hsv[2] < value_threshold:
            # 根据接近程度设置透明度，这里简单地用固定值设置，你也可以根据更复杂的逻辑来设置
            alpha = 0
            new_data.append((item[0], item[1], item[2], alpha))
        else:
            new_data.append(item)

    # 更新图片的像素数据
    image.putdata(new_data)

    # 保存为PNG格式，PNG支持透明度
    image.save(output_image_path, "PNG")


if __name__ == "__main__":
    input_image_path = r"E:\AI数字人\logos\logo.jpg"  # 替换为你的输入图片路径
    output_image_path = r"E:\AI数字人\logos\logo.png"  # 替换为你想要保存的输出图片路径
    removeDarkWithTransparent(input_image_path, output_image_path)
    