import os
import json

"""
 这是端口替换，如有需要记得保留原有的端口
 注意备份! 注意备份! 注意备份! 
 
"""
myport = {
    "0": {
        "inside": 22,
        "host": 10022
    },
    # "1": {
    #     "inside": 80,
    #     "host": 10080
    # }
}

"""
docker ps # 查看目标容器的container-id

/var/lib/docker/containers/<container-id>
"""
container_dir = "/var/lib/docker/containers/356d4dd03ec9506dea065200f4269c705997f33df18f386f977333b8d484bc17"

hostconfig_json_path = os.path.join(container_dir, "hostconfig.json")
config_v2_json_path = os.path.join(container_dir, "config.v2.json")

if __name__ == '__main__':
    os.system("systemctl stop docker")

    with open(hostconfig_json_path, "r", encoding='utf8') as f:
        hostconfig = json.load(f)

    with open(config_v2_json_path, "r", encoding='utf8') as f:
        config_v2 = json.load(f)

    for val in myport.values():
        inside_port = val["inside"]
        host_port = val["host"]
        key = "%s/tcp" % inside_port

        hostconfig["PortBindings"][key] = [{"HostIp": "", "HostPort": "%s" % host_port}]

        config_v2["Config"]["ExposedPorts"] = {}
        config_v2["Config"]["ExposedPorts"][key] = {}

        config_v2["NetworkSettings"]["Ports"] = {}
        config_v2["NetworkSettings"]["Ports"][key] = [
            {"HostIp": "0.0.0.0", "HostPort": "%s" % host_port}]

    with open(hostconfig_json_path, "w", encoding='utf8') as f:
        f.write(json.dumps(hostconfig, ensure_ascii=False))

    with open(config_v2_json_path, "w", encoding='utf8') as f:
        f.write(json.dumps(config_v2, ensure_ascii=False))

    os.system("systemctl start docker")

