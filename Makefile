.PHONY: package

package:
	tar -czvf gemini-proxy-service.tar.gz \
		gemini-proxy-service/Dockerfile \
		gemini-proxy-service/key_manager.py \
		gemini-proxy-service/main.py \
		gemini-proxy-service/requirements.txt \
		gemini-proxy-service/web_interface.py \
		gemini-proxy-service/templates/keys_table.html \
		gemini-proxy.service \
		docker-compose.yml