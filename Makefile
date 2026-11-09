cat:
	cat Makefile

git:
	git add .
	git commit -m "jelly  work 2026 fall"
	git push


jelly:
	#not docker compose up -d
	./run_jelly.sh



dirs:
	mkdir -p ./jellyfin/config ./jellyfin/cache
