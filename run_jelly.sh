  #--net=host \ \
docker kill jellyfin
docker rm jellyfin
docker run -d \
  --name=jellyfin \
  -p 8096:8096 \
  -e PUID=1002 \
  -e PGID=1002 \
  -e COMPlus_EnableDiagnostics=0\
  -v /home/tony/work/jelly/jellyfin/config:/config \
  -v /home/tony/work/jelly/jellyfin/cache:/cache \
  -v /mnt/plexLive/0_Music:/media/music:ro \
  --restart unless-stopped \
docker.io/linuxserver/jellyfin:latest

