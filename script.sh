docker tag price-comparison-system-celery-beat:latest zhouyueer/price-comparison-system-celery-beat:latest
docker tag price-comparison-system-celery:latest zhouyueer/price-comparison-system-celery:latest
docker tag price-comparison-system-vue:latest zhouyueer/price-comparison-system-vue:latest
docker tag price-comparison-system-nginx:latest zhouyueer/price-comparison-system-nginx:latest
docker push zhouyueer/price-comparison-system-flask:latest
docker push zhouyueer/price-comparison-system-celery-beat:latest
docker push zhouyueer/price-comparison-system-celery:latest
docker push zhouyueer/price-comparison-system-vue:latest
docker push zhouyueer/price-comparison-system-nginx:latest
