
import requests


class DellR410Info:
    temperature = None
    speed = None

    def __init__(self):
        self.temperature: float
        self.speed: float


class DellR410Node12CpuMemInfo:
    cpu: float = None
    cpuDesc: float = None
    mem: float = None
    memDesc: float = None


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


def getNode12CpuMemInfo() -> DellR410Node12CpuMemInfo:
    resp = requests.get(
        'http://192.168.0.101:5000/get_node12_cpu_mem_df_info')
    # {
    #     "cpu": "16.0",
    #     "cpuDesc": " root 16.0 0.1 /usr/local/bin/ffmpeg -v info -t 77572 -i rtsp://admin:AGXXZI@192.168.0.105:554/h264/ch1/sub/av_stream -force_key_frames expr:gte(t,n_forced*1) -hls_time 60 -threads 1 -hls_list_size 0 -hls_segment_filename /ssxtmp/index_1690223228_%20d.ts /ssxtmp/index_1690223228.m3u8 \n",
    #     "mem": "3.4",
    #     "memDesc": " root 0.8 3.4 java -DuserLogbackLevel=error -Dloader.path=/home/app/apps/k8s/for_docker_volume/jenkins/jars/eureka-server -jar /myappjar/app.jar --spring.profiles.active=prod \n"
    # }
    if resp.status_code != 200:
        raise IOError('请求node12内存处理器信息Python接口失败！！')
    respJson = resp.json() #{"fanSpeed":"7920","temperature":32}
    d2 = DellR410Node12CpuMemInfo()
    d2.cpu = respJson['cpu']
    d2.cpuDesc = respJson['cpuDesc']
    d2.mem = respJson['mem']
    d2.memDesc = respJson['memDesc']
    return d2


if __name__ == '__main__':
    a = getDellR410Info()
    print(a.temperature)
    print(a.speed)
