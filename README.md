# BrightcovePlayer
docker run --restart always --name player -d --mount type=bind,src='/etc/ssl/bundle.pem',dst=/docker-entrypoint.d/bundle.pem —env-file ~/bcp.env -p 8080:80 -p 4443:443 deshdeepak1/bcp:latest
