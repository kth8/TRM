# Transmission Remove
Docker container to automatically remove completed Transmisson torrents every 15 minutes. If the Transmission daemon is running on the host with IP address of `192.168.0.2`:
```
docker run -d \
  --name trm \
  --restart always \
  -e TRANSMISSION_HOST=192.168.0.2 \
  -e TRANSMISSION_PORT=9091 \
  ghcr.io/kth8/trm
```
set `-e TRANSMISSION_HOST=192.168.0.2` to the IP address your Transmission daemon is accessible on. Make sure RPC access is probably configured to allow external access.
