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
        'http://192.168.0.101:5000/autoSetDellFanOnceTempAndSpeed')
    # {'temperature': '30', 'speed': 8448.0}
    if resp.status_code != 200:
        raise IOError('请求dell风扇转速Python接口失败！！')
    respJson = resp.json() #{"fanSpeed":"7920","temperature":32}
    d = DellR410Info()
    d.temperature = respJson['temperature']
    d.speed = respJson['fanSpeed']
    return d


def getNode12CpuMemInfo():
    resp = requests.get(
        'http://192.168.0.101:5000/get_node12_cpu_mem_df_info')
    # {'temperature': '30', 'speed': 8448.0}
    if resp.status_code != 200:
        raise IOError('请求node12内存处理器信息Python接口失败！！')
    respJson = resp.json() #{"fanSpeed":"7920","temperature":32}
    return respJson


if __name__ == '__main__':
    a = getDellR410Info()
    print(a.temperature)
    print(a.speed)
