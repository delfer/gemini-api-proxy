.PHONY: package

package:
	tar -czvf gemini-proxy-service.tar.gz \
		Dockerfile \
		key_manager.py \
		main.py \
		requirements.txt \
		web_interface.py \
		keys_table.html \
		systemd-services/gemini-proxy.service \
		docker-compose.yml