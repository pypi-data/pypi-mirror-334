sudo systemctl restart sshd
3.235.142.37:8443 # rancher 

####
sudo docker run --privileged -d \
  --restart=always \
  -p 8081:80 -p 8443:443 \
  rancher/rancher
############################

# 
docker logs  container-id  2>&1 | grep "Bootstrap Password:"
###