FROM nginx:stable

COPY default.conf /etc/nginx/sites-available/ttm4115-e-scooter-application.conf
COPY docker/nginx/apply-project.sh /apply-project.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
