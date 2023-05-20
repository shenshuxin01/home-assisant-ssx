import json

import requests


class DellR410Info:
    temperature = None
    speed = None

    def __init__(self):
        self.temperature: float
        self.speed: float


def getDellR410Info() -> DellR410Info:
    resp = requests.get(
        'http://192.168.0.101:30501/developer-function-provider/setDellFan/test/getFanSpeedAndTemperature')
    # {'temperature': '30', 'speed': 8448.0}
    if resp.status_code != 200:
        raise IOError('请求dell风扇转速接口失败！！')
    respJson = resp.json()
    d = DellR410Info()
    d.temperature = respJson['temperature']
    d.speed = respJson['speed']
    return d


if __name__ == '__main__':
    a = getDellR410Info()
    print(a.temperature)
    print(a.speed)
