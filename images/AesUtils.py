import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# 密钥,建议动态配置
SECRET_KEY = 'Ir9rzSfhykygH4dXH4CCEK0MghnyM8df'  # 此处16|24|32个字符

class AesUtils:

    @staticmethod
    def encrypt(sSrc, sKey):
        """
        加密

        :param sSrc: 明文字符串
        :param sKey: 密钥字符串（16或32字节）
        :return: 加密后的16进制字符串
        """
        if sKey is None:
            print("Key为空null")
            return None
        if len(sKey) != 16 and len(sKey) != 32:
            print("Key长度不是16位 或者 32")
            return None

        try:
            raw = sKey.encode('utf-8')
            cipher = AES.new(raw, AES.MODE_ECB)
            padded_data = pad(sSrc.encode('utf-8'), AES.block_size, style='pkcs7')
            encrypted = cipher.encrypt(padded_data)
            return AesUtils.parse_byte2hex_str(encrypted)
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def decrypt(sSrc, sKey):
        """
        解密

        :param sSrc: 加密的16进制字符串
        :param sKey: 密钥字符串（16或32字节）
        :return: 解密后的明文字符串
        """
        if sKey is None:
            print("Key为空null")
            return None
        if len(sKey) != 16 and len(sKey) != 32:
            print("Key长度不是16位 或者 32")
            return None

        try:
            raw = sKey.encode('utf-8')
            cipher = AES.new(raw, AES.MODE_ECB)
            encrypted = AesUtils.parse_hex_str2byte(sSrc)
            original = unpad(cipher.decrypt(encrypted), AES.block_size, style='pkcs7')
            return original.decode('utf-8')
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def parse_byte2hex_str(buf):
        """
        将二进制转换成16进制

        :param buf: 字节数组
        :return: 16进制字符串
        """
        return binascii.hexlify(buf).decode('utf-8').upper()

    @staticmethod
    def parse_hex_str2byte(hexStr):
        """
        将16进制转换为二进制

        :param hexStr: 16进制字符串
        :return: 字节数组
        """
        return binascii.unhexlify(hexStr)


if __name__ == '__main__':

    # 请求例子数据
    dict_value = {
        'appId': '1826095723125543000',
        'realTenant': '123',
        'virtualTenant':'123',
        'enterpriseId': 'ali123',
        'userId': 'ali123',
        'enterpriseName': '123',
        'userName': 'ali123',
        'userPhone': '123'
    }
    encrypted_text = AesUtils.encrypt(str(dict_value), SECRET_KEY)
    print(encrypted_text)
    # 对应知识库数据;从AI管理后台获取联系对应人员获取
    request_data = {
        "appId": "1826095723125543000",
        "appKey": "7Qyb4kItmdunYE3g",
        "data": encrypted_text
    }
    headers = {
        'Content-type': 'application/json'
    }
    print(json.dumps(request_data))
    resp_data = requests.post("http://172.21.129.228:9203/business/aiSession/addOrGet", data=json.dumps(request_data),headers=headers)
    print(resp_data.text)