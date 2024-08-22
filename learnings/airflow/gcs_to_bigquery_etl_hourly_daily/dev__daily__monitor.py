import os
from datetime import timedelta, datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.slack.operators.slack import SlackAPIPostOperator

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
translate_table = str.maketrans(" :-", "___")
translate_partition = str.maketrans(":-", "  ")

environment = "dev"
data_frequency = "daily"
gcs_file_format = "AVRO"
gcs_success_file = "_SUCCESS"
project_name = "PROJECT_NAME"
team_name = "PROJECT_NAME"
location = "europe-west2"

project_id = "PROJECT_ID"
dataset_id = "DATASET_ID"
gcs_bucket = "BUCKET_NAME"
feed_name = "FEED_NAME"

slack_channel_id = "CXXXXXX"  # develop
slack_conn_id = "slack_api_default"  # Created via Google Cloud Composer Airflow UI
slack_username = "Demo_ETL"

dag_id = f"{os.path.basename(__file__).replace('.py', '')}"
gcs_prefix = f"{feed_name}/"
table_slug = feed_name.translate(translate_table)
raw_table_id = f"raw__{table_slug}__{data_frequency}"
labels = {"env": environment, "project": project_name, "team": team_name}
pipeline_dag_id = (
    f"{environment}__{project_name}__{table_slug}__{data_frequency}__pipeline"
)

# SQL Query to get the bigquery table partitions
get_raw_table_partition_query = f"""
SELECT
    partition_id
FROM
    `{project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS`
WHERE
    table_name = '{raw_table_id}';"""

# SQL Query for identifying the partition gap
identify_missing_partition_query = f"""
WITH 
    raw AS (
        SELECT
            partition_id
        FROM
            `{project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS`
        WHERE
            table_name = '{raw_table_id}'
            AND partition_id <> '__NULL__'
    ),
    expected AS (
        SELECT
            FORMAT_DATE("%Y%m%d", date) AS partition_id
        FROM
            UNNEST(
                GENERATE_DATE_ARRAY(
                    '2024-01-01',
                    DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY), -- TIMEDELTA
                    INTERVAL 1 DAY
                )
            ) AS date
    )
SELECT
    expected.partition_id
FROM
    expected LEFT JOIN raw ON raw.partition_id = expected.partition_id
WHERE
    raw.partition_id IS NULL
    AND expected.partition_id >= (
        SELECT
            COALESCE(MIN(partition_id), FORMAT_DATE("%Y%m%d", CURRENT_DATE()))
        FROM
            `{project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS`
        WHERE
            table_name = '{raw_table_id}'
            AND partition_id <> '__NULL__'
    );
"""
# -----------------------------------------------------------------------------
# DAG Init
# -----------------------------------------------------------------------------

default_args = {
    "owner": f"{team_name.upper()}",
    "start_date": days_ago(1),
    "retries": 0,
    "retry_delay": timedelta(hours=1),
    "execution_timeout": timedelta(minutes=30),
    "depends_on_past": False,
}

dag = DAG(
    dag_id=dag_id,
    description=f"A DAG to monitor the {project_name.capitalize()} file landing path in GCS and initiate the ETL DAG pipeline.",
    default_args=default_args,
    schedule=timedelta(hours=1),
    catchup=False,
    max_active_runs=1,
    tags=[environment, project_name, "etl", table_slug, data_frequency],
)


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def get_gcs_partition(**kwargs):
    """fetches the gcs partition list from `scan_gcs_bucket` task and filter the successfully uploaded partition folders."""
    ti = kwargs["ti"]
    folders = [
        os.path.dirname(object)
        for object in ti.xcom_pull(task_ids="scan_gcs_bucket")
        if object.endswith(gcs_success_file)
    ]
    storage_partition = [item.split("/")[1] for item in folders]
    print(f"\t{storage_partition=}")
    ti.xcom_push(key="storage_partition", value=storage_partition)


def check_partition_exists(job_id, **kwargs):
    """compare the gcs parition and bigquery table partition to get the latest/new partition list."""
    print(f"\t BigQuery Job ID: {job_id}")

    ti = kwargs["ti"]
    hook = BigQueryHook()
    client = hook.get_client(project_id=project_id, location=location)
    query_results = client.get_job(job_id).result()

    bq_partition = [
        datetime.strptime(row.get("partition_id"), "%Y%m%d%H").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        for row in query_results
        if row.get("partition_id", "__NULL__") not in ["__NULL__"]
    ]
    bq_partition.sort()
    print(f"\t{bq_partition=}")

    storage_partition = ti.xcom_pull(
        task_ids="get_gcs_partition", key="storage_partition"
    )
    storage_partition.sort()
    print(f"\t{storage_partition=}")

    # Identify the new partitions
    new_storage_partition = list(set(storage_partition) - set(bq_partition))
    new_storage_partition.sort()
    print(f"\t{new_storage_partition=}")
    ti.xcom_push(key="new_storage_partition", value=new_storage_partition)


def trigger_dags(**kwargs):
    """triggers the ETL pipeline DAG with partition_key"""
    ti = kwargs["ti"]
    partition_keys = ti.xcom_pull(
        task_ids="check_new_partition", key="new_storage_partition"
    )

    for partition_key in partition_keys:
        print({"parition_key": partition_key})
        TriggerDagRunOperator(
            task_id=f"pipeline_dag__{partition_key.translate(translate_table)}",
            trigger_dag_id=pipeline_dag_id,
            conf={"partition_key": partition_key},
            dag=dag,
        ).execute(context=kwargs)


def identify_partition_gap(**kwargs):
    """Checks for the partition gap and notifies in slack channel if any gap is found."""
    ti = kwargs["ti"]
    print(identify_missing_partition_query)
    hook = BigQueryHook(location=location, use_legacy_sql=False, labels=labels)
    df = hook.get_pandas_df(identify_missing_partition_query)
    missing_partitions = df["partition_id"].tolist()
    print(f"\t{missing_partitions}")
    if len(missing_partitions):
        message = f"""{dag_id} | {project_id} | {dataset_id} | {raw_table_id} | Partition gap identified | Total - {len(missing_partitions)} - {missing_partitions}"""
        ti.xcom_push(key="slack_message", value=message)
        return "send_alert"
    return "ignore_alert"


# -----------------------------------------------------------------------------
# DAG Tasks
# -----------------------------------------------------------------------------


scan_gcs_bucket_task = GCSListObjectsOperator(
    task_id="scan_gcs_bucket",
    bucket=gcs_bucket,
    prefix=gcs_prefix,
    match_glob=f"**/*/{gcs_success_file}",
    dag=dag,
)


get_gcs_partition_task = PythonOperator(
    task_id="get_gcs_partition",
    python_callable=get_gcs_partition,
    provide_context=True,
    dag=dag,
)

get_bq_partition_task = BigQueryInsertJobOperator(
    task_id="get_bq_partition",
    configuration={
        "query": {
            "query": get_raw_table_partition_query,
            "useLegacySql": False,
        }
    },
    location=location,
    project_id=project_id,
    dag=dag,
)

check_new_partition_task = PythonOperator(
    task_id="check_new_partition",
    python_callable=check_partition_exists,
    op_args=["{{ task_instance.xcom_pull(task_ids='get_bq_partition') }}"],
    provide_context=True,
    dag=dag,
)

trigger_dag_task_loop = PythonOperator(
    task_id="trigger_dag_loop",
    python_callable=trigger_dags,
    provide_context=True,
    dag=dag,
)

identify_partition_gap_task = BranchPythonOperator(
    task_id="identify_partition_gap",
    python_callable=identify_partition_gap,
    dag=dag,
)

send_alert_task = SlackAPIPostOperator(
    task_id="send_alert",
    text="{{ task_instance.xcom_pull(key='slack_message') }}",
    channel=slack_channel_id,
    username=slack_username,
    dag=dag,
)


ignore_alert_task = DummyOperator(
    task_id="ignore_alert",
    dag=dag,
)
# -----------------------------------------------------------------------------
# DAG's Tasks Dependencies (ie execution order)
# -----------------------------------------------------------------------------

(
    scan_gcs_bucket_task
    >> get_gcs_partition_task
    >> get_bq_partition_task
    >> check_new_partition_task
    >> trigger_dag_task_loop
    >> identify_partition_gap_task
    >> [send_alert_task, ignore_alert_task]
)
