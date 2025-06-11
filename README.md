# Modern Data Engineering Stack Practice

This project provides a comprehensive, local development environment for practicing modern data engineering workflows using Docker. It integrates key technologies like Hadoop, Spark, Kafka, and Airflow into a cohesive, ready-to-run stack.

## Architecture

The architecture is designed to simulate a real-world data pipeline, from data ingestion to processing and orchestration.

```mermaid
graph TD
    subgraph "Data Sources"
        A[Python Producer Script]
    end
    
    subgraph "Data Ingestion & Streaming"
        B(Kafka KRaft Cluster)
    end

    subgraph "Data Lake Storage (HDFS)"
        D[NameNode]
        E[DataNode]
        D -- Manages --> E
    end
    
    subgraph "Data Processing"
        F[Spark Cluster]
    end

    subgraph "Workflow Orchestration"
        G[Airflow]
    end
    
    A -- Pushes Events --> B
    G -- Triggers & Monitors --> F
    F -- Reads from --> B
    F -- Writes to --> D
```

## Technologies

- **Orchestration**: Apache Airflow `2.9.2`
- **Processing**: Apache Spark `3.5.1`
- **Streaming**: Apache Kafka `3.7.0` (KRaft Mode)
- **Storage**: Apache Hadoop `3.4.0` (HDFS)
- **Database**: PostgreSQL `16`
- **Containerization**: Docker & Docker Compose

## Key Features

- **Pre-configured Spark**: Custom Docker image with Delta Lake and Kafka dependencies pre-installed
- **Streaming Support**: Real-time data processing with Spark Structured Streaming
- **Delta Lake Integration**: ACID transactions and time travel capabilities
- **Fault Tolerance**: Checkpoint mechanisms for stream recovery
- **Production Ready**: Proper HDFS permissions and security configurations

    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create Directory Structure**
    Ensure the following directories exist in your project root. They are mounted as volumes into the containers.
    ```bash
    mkdir -p ./dags ./logs ./plugins ./scripts ./config/hadoop
    ```

3.  **Create Hadoop Configuration**
    Create `core-site.xml` and `hdfs-site.xml` inside the `./config/hadoop/` directory as specified in the project documentation.

4.  **Set Up Environment Variables**
    Copy the example `.env` file and customize it.
    ```bash
    cp .env.example .env
    ```
    **Important:** For Linux/macOS users, update `AIRFLOW_UID` in the `.env` file with the output of the `id -u` command to avoid file permission issues.
    ```bash
    echo "AIRFLOW_UID=$(id -u)" >> .env
    ```
5. **Format HDFS NameNode (First Time Only)**
    ```bash
    docker-compose run --rm namenode hdfs namenode -format
    ```
    > **Important:** This step initializes the HDFS filesystem, similar to formatting a new hard drive.
    > This command is mandatory for the first launch but should NOT be run again, as it will erase all HDFS metadata.

## Usage

- **Start all services in the background:**
  ```bash
  docker-compose up -d --build
  ```

- **Check the status of all services:**
  ```bash
  docker-compose ps
- **Build and start all services (required for first run or after changes):**

- **View logs for a specific service (e.g., airflow-webserver):**
  ```bash
  docker-compose logs -f airflow-webserver
- **Start all services (using existing images):**
  ```bash
  docker-compose up -d
  ```

  ```

## Service Endpoints

Once the stack is running, you can access the UIs at the following endpoints:

| Service | URL | Credentials |
| :--- | :--- | :--- |
| **Airflow Web UI** | `http://localhost:8081` | `admin` / `admin` |
| **Spark Master UI**| `http://localhost:8080` | N/A |
| **HDFS NameNode UI**| `http://localhost:9870` | N/A |

## Next Steps

1.  Write a Python script in the `./scripts` directory to produce messages to a Kafka topic.
2.  Develop a PySpark application in `./scripts` to process the data from Kafka.
3.  Create an Airflow DAG in the `./dags` directory to orchestrate the entire workflow.

## Running Spark Jobs

With the custom Spark image, you can now run streaming jobs with Delta Lake and Kafka support using a simple command:

```bash
# Simple command - dependencies already included in the image
docker-compose exec spark-master spark-submit /opt/bitnami/spark/scripts/process_city_events.py
```

**✅ No need for additional packages or configurations** - everything is pre-installed!

### Alternative: Manual Package Loading (if needed)
```bash
# Fallback method with manual dependency download
docker-compose exec spark-master spark-submit \
  --packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0" \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  /opt/bitnami/spark/scripts/process_city_events.py
```

## Docker Images

### Custom Spark Image ✅ **WORKING**
Located in `./docker/spark/Dockerfile`, this image extends the official Bitnami Spark image with:
- **Kafka Integration**: `spark-sql-kafka` and related dependencies (Scala 2.12)
- **Delta Lake**: `delta-spark` and `delta-storage` libraries  
- **Pre-installed JARs**: All dependencies downloaded during build time
- **Version Compatibility**: Correct versions for Spark 3.5.1

Benefits of the custom image:
- ✅ **Faster Startup**: No dependency download time
- ✅ **Offline Capability**: Works without internet connection
- ✅ **Version Consistency**: Locked dependency versions
- ✅ **Production Ready**: Optimized for performance
- ✅ **Simple Commands**: No complex parameter passing needed
