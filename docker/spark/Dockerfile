# ./docker/spark/Dockerfile (Fixed Version with Better Error Handling)

# Start from the official Bitnami Spark image that we trust
FROM bitnami/spark:3.5.1

# Switch to root user to get permissions to install software
USER root

#
# --- INSTALL REQUIRED TOOLS ---
#
RUN apt-get update && \
    apt-get install -y wget curl && \
    rm -rf /var/lib/apt/lists/*

#
# --- DOWNLOAD AND INSTALL DEPENDENCIES ---
# Create a temporary directory for downloads
#
RUN mkdir -p /tmp/jars && \
    cd /tmp/jars && \
    echo "Downloading Kafka integration JARs..." && \
    wget -v https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar && \
    wget -v https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.1/spark-token-provider-kafka-0-10_2.12-3.5.1.jar && \
    wget -v https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.1/kafka-clients-3.4.1.jar && \
    wget -v https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
    echo "Downloading Delta Lake JARs..." && \
    wget -v https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.0/delta-spark_2.12-3.2.0.jar && \
    wget -v https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar && \
    wget -v https://repo1.maven.org/maven2/org/antlr/antlr4-runtime/4.9.3/antlr4-runtime-4.9.3.jar && \
    echo "Listing downloaded files:" && \
    ls -la /tmp/jars/ && \
    echo "Moving JARs to Spark directory..." && \
    cp /tmp/jars/*.jar /opt/bitnami/spark/jars/ && \
    chown 1001:root /opt/bitnami/spark/jars/*.jar && \
    echo "Verifying JARs in Spark directory:" && \
    ls -la /opt/bitnami/spark/jars/ | grep -E "(delta|kafka|commons-pool)" && \
    rm -rf /tmp/jars

#
# --- FINAL SECURITY STEP ---
# Switch back to the non-root spark user for better security practices.
#
USER 1001