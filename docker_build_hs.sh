mkdir -p /root/docker-volume/hass/{config,media}

docker rm -f `docker ps -qa -f name=homeassistant`

docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /root/docker-volume/hass/config:/config \
  -v /run/dbus:/run/dbus:ro \
  -v /root/hass_ssh/.ssh:/root/.ssh \
  --network=host registry.cn-hangzhou.aliyuncs.com/ssx-pub/home-assistant:2024.6.4-amd
