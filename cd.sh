remote_ha=/root/docker-volume/hass/config
remote_user=root@192.168.0.102

scp configuration.yaml start.sh ${remote_user}:${remote_ha} \
  && ssh ${remote_user} "rm -rf ${remote_ha}/custom_components/{edge_tts,hass_cozylife_local_pull,ssx_hass}" \
  && scp -r custom_components/*  ${remote_user}:${remote_ha}/custom_components \
  && ssh ${remote_user} "bash ${remote_ha}/start.sh"

