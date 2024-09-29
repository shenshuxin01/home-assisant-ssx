mkdir -p /root/docker-volume/hass/{config,media}

docker rm -f `docker ps -qa -f name=homeassistant`

docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /root/docker-volume/hass/config:/config \
  -v /run/dbus:/run/dbus:ro \
  --network=host swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/home-assistant/home-assistant:stable
