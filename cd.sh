nd1_hass=/home/app/apps/k8s/for_docker_volume/homeassistant/config

scp configuration.yaml secrets.yaml  root@node101:${nd1_hass} \
  && ssh root@node101 "rm -rf ${nd1_hass}/custom_components/example_load_platform" \
  && scp -r ./custom_components/example_load_platform  root@node101:${nd1_hass}/custom_components \
  && ssh root@node101 "kubectl delete pod -n ssx \`kubectl get pod -n ssx | grep homeassistant | awk '{print \$1}'\`"

