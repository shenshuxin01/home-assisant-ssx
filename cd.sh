nd1_hass=/home/app/apps/k8s/for_docker_volume/homeassistant/config

scp configuration.yaml secrets.yaml  root@node109:${nd1_hass} \
  && ssh root@node109 "rm -rf ${nd1_hass}/custom_components/example_load_platform" \
  && scp -r ./custom_components/example_load_platform  root@node109:${nd1_hass}/custom_components \
  && ssh root@node109 "kubectl delete pod -n ssx \`kubectl get pod -n ssx | grep homeassistant | awk '{print \$1}'\`"

