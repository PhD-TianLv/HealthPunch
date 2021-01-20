from aip import AipOcr
import Settings as settings

""" 你的 APPID AK SK """
APP_ID = settings.APP_ID
API_KEY = settings.API_KEY
SECRET_KEY = settings.SECRET_KEY

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {"language_type": "ENG"}


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def VCodeRec(filePath):
    """
    调用百度 OCR 识别验证码
    :param filePath: 验证码图片的保存地址
    :return: 验证码识别结果
    """
    image = get_file_content(filePath)
    ocr_result = client.basicAccurate(image, options)
    try:
        word = ocr_result['words_result'][0]['words'].replace(" ", "")
    except IndexError:
        word = ""
    finally:
        return word
