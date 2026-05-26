import math
import socket
import struct

UDP_IP = "0.0.0.0"
UDP_PORT = 8000

# dat类型 -> struct格式  https://github.com/richstokes/Forza-data-tools/blob/master/FH4_packetformat.dat
TYPE_MAP = {
    "f32": ("f", 4),
    "u32": ("I", 4),
    "s32": ("i", 4),
    "u16": ("H", 2),
    "u8": ("B", 1),
    "s8": ("b", 1),

    # unknown horizon field
    "hzn": (None, 4),
}


def load_dat_file(path):
    fields = []
    offset = 0
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().replace(';', '')
        # 去掉注释
        comment = ''
        if "//" in line:
            line_s = line.split("//")
            line = line_s[0].strip()
            comment = line_s[1].strip()
        # 跳过空行
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2:
            continue
        type_name, field_name = parts
        if type_name not in TYPE_MAP:
            print(f"未知类型: {type_name}")
            continue
        fmt, size = TYPE_MAP[type_name]
        fields.append({
            "comment": comment,
            "name": field_name,
            "fmt": fmt,
            "size": size,
            "offset": offset
        })
        offset += size
    return fields


def parse_packet(data, fields):
    result = {}

    for field in fields:
        value = struct.unpack_from(
            "<" + field["fmt"],
            data,
            field["offset"]
        )[0]

        result[field["name"]] = value

    return result


def udp_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    fields = load_dat_file('./FH4_packetformat.dat')
    print("等待数据...")

    while True:
        data, addr = sock.recvfrom(1500)

        telemetry = parse_packet(data, fields)
        for e in fields:
            value=telemetry[e["name"]]
            # print(f"{e['name']}: {value} //comment{e['comment']}")


        # 速度 (m/s)
        speed = telemetry["Speed"]

        # 发动机转速
        rpm = telemetry["CurrentEngineRpm"]

        # 当前档位
        gear = telemetry["Gear"]

        kmh = speed * 3.6
        print(f"speed: {math.trunc(kmh)} km/h, rpm: {math.trunc(rpm)}转速, gear: {gear} 档")



if __name__ == '__main__':
    udp_packet()
