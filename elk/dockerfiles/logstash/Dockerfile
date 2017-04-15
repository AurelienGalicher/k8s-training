FROM logstash:5.2.2
MAINTAINER galicher@gmail.com

# Install Kibana plugins
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-kafka
RUN /logstash-plugin install logstash-filter-json && /usr/share/logstash/bin/logstash

# Mount volume to get config files
VOLUME ["/lostash/config"]

# Entrypoint
ENTRYPOINT ["/usr/share/logstash/bin/logstash", "-f", "/logstash/config/logstash.conf"]

