remote_ha=/root/docker-volume/hass/config
remote_user=root@192.168.0.102

scp configuration.yaml docker_build_hs.sh ${remote_user}:${remote_ha} \
  && ssh ${remote_user} "rm -rf ${remote_ha}/custom_components/{edge_tts,hass_cozylife_local_pull,ssx_hass,xiaomi_miot}" \
  && scp -r custom_components/*  ${remote_user}:${remote_ha}/custom_components \
  && ssh ${remote_user} "bash ${remote_ha}/docker_build_hs.sh"

