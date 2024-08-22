import os
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.exceptions import AirflowException
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryDeleteTableOperator,
    BigQueryInsertJobOperator,
)
from airflow.providers.slack.operators.slack import SlackAPIPostOperator

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
translate_table = str.maketrans(" :-", "___")
translate_partition = str.maketrans(":-", "  ")

environment = "dev"
data_frequency = "daily"
gcs_file_format = "AVRO"
project_name = "PROJECT_NAME"
team_name = "TEAM_NAME"
location = "europe-west2"
project_id = "PROJECT_ID"
dataset_id = "DATASET_ID"
feed_name = "FEED_NAME"
gcs_bucket = "BUCKET_NAME"

slack_channel_id = "CXXXXXXX"  # develop
slack_conn_id = "slack_api_default"  # Created via Google Cloud Composer Airflow UI
slack_username = "Demo_ETL"

dag_id = f"{os.path.basename(__file__).replace('.py', '')}"
labels = {"env": environment, "project": project_name, "team": team_name}

delete_partition_from_table_query = """DELETE `{project_id}.{dataset_id}.{raw_table_id}` WHERE partition_key = DATE_TRUNC("{partition_key}", DAY);"""

insert_into_table_query = """
INSERT INTO
    `{project_id}.{dataset_id}.{raw_table_id}`  (
    view_id,
    view_name,
    file_id,
    file_name,
    dt,
    partition_key
    )
SELECT
    view_id,
    view_name,
    file_id,
    file_name,
    dt, DATE_TRUNC("{partition_key}", DAY) as partition_key
FROM
    `{temp_table_uri}`;
"""

raw_table_partition_count_query = """
SELECT
    total_rows as total
FROM
    `{project_id}.{dataset_id}.INFORMATION_SCHEMA.PARTITIONS`
WHERE
    table_name = '{raw_table_id}' and partition_id = '{bq_parition_key}' ;
"""

temp_table_count_query = """
SELECT
    count(*) as total
FROM
    `{temp_table_uri}`
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
    description=f"A DAG to perform ETL from GCS bucket({data_frequency}) to BigQuery",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    render_template_as_native_obj=True,
    tags=[
        environment,
        project_name,
        "etl",
        feed_name.translate(translate_table),
        data_frequency,
    ],
)


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def set_xcom_variables(**kwargs):
    """read partition_key from params and sets the xcom variables"""
    ti = kwargs["ti"]
    print(kwargs)
    print(f"\t{kwargs['params']}")
    params = kwargs["params"]
    print(params)
    partition_key = params.get("partition_key", None)
    if not partition_key:
        message = f"""{dag_id} | {project_id} | {dataset_id} | Partition Key Missing"""
        print(message)
        ti.xcom_push(key="slack_message", value=message)
        raise AirflowException(f"Partition key missing in params.{kwargs['params']}")

    print(params.get("partition_key", None))
    gcs_prefix = f"{feed_name}/{partition_key}/*.avro"
    table_slug = feed_name.translate(translate_table)
    bq_parition_key = partition_key.translate(translate_partition).replace(" ", "")[:10]
    raw_table_id = f"raw__{table_slug}__{data_frequency}"
    raw_flat_table_id = f"raw__{table_slug}__flat__{data_frequency}"
    temp_table_id = f"tmp__{table_slug}__{data_frequency}__{partition_key.translate(translate_table)}"
    temp_table_uri = f"{project_id}.{dataset_id}.{temp_table_id}"

    kv = dict(
        project_id=project_id,
        dataset_id=dataset_id,
        raw_table_id=raw_table_id,
        raw_flat_table_id=raw_flat_table_id,
        partition_key=partition_key,
        bq_parition_key=bq_parition_key,
        temp_table_uri=temp_table_uri,
        temp_table_id=temp_table_id,
    )

    ti.xcom_push(key="raw_table_id", value=raw_table_id)
    ti.xcom_push(key="raw_flat_table_id", value=raw_flat_table_id)
    ti.xcom_push(key="temp_table_id", value=temp_table_id)
    ti.xcom_push(key="partition_key", value=partition_key)
    ti.xcom_push(key="gcs_prefix", value=gcs_prefix)
    ti.xcom_push(key="temp_table_uri", value=temp_table_uri)
    ti.xcom_push(
        key="delete_partition_from_table_query",
        value=delete_partition_from_table_query.format(**kv),
    )
    ti.xcom_push(
        key="insert_into_table_query", value=insert_into_table_query.format(**kv)
    )
    ti.xcom_push(
        key="raw_table_partition_count_query",
        value=raw_table_partition_count_query.format(**kv),
    )
    ti.xcom_push(
        key="temp_table_count_query", value=temp_table_count_query.format(**kv)
    )


def validate_schema(**kwargs):
    """Checks for Schema consistency"""
    ti = kwargs["ti"]
    temp_table_id = ti.xcom_pull(key="temp_table_id")
    raw_table_id = ti.xcom_pull(key="raw_table_id")
    hook = BigQueryHook(location=location, use_legacy_sql=False, labels=labels)
    temp_table_schema = hook.get_schema(
        dataset_id=dataset_id, table_id=temp_table_id, project_id=project_id
    )
    raw_table_schema = hook.get_schema(
        dataset_id=dataset_id, table_id=raw_table_id, project_id=project_id
    )

    print(f"{type(temp_table_schema)} {temp_table_schema=}")
    print(f"{type(raw_table_schema)} {raw_table_schema=}")

    # remove the 'partition_key' in the raw schema
    raw_table_schema["fields"] = [
        _d
        for _d in raw_table_schema["fields"]
        if _d.get("name", "partition_key") != "partition_key"
    ]

    if temp_table_schema == raw_table_schema:
        print("Schema Matches")
        return "insert_into_raw_table"
    else:
        message = f"""{dag_id} | {project_id} | {dataset_id} | {raw_table_id} | {temp_table_id} | Schema Mismatch identified"""
        ti.xcom_push(key="slack_message", value=message)
        raise AirflowException(message)


def validate_data_count(**kwargs):
    """Checks the data count in temp table and raw table(partition)"""
    ti = kwargs["ti"]
    hook = BigQueryHook(location=location, use_legacy_sql=False, labels=labels)

    temp_table_id = ti.xcom_pull(key="temp_table_id")
    raw_table_id = ti.xcom_pull(key="raw_table_id")
    raw_table_partition_count_query = ti.xcom_pull(
        key="raw_table_partition_count_query"
    )
    temp_table_count_query = ti.xcom_pull(key="temp_table_count_query")

    raw_result_df = hook.get_pandas_df(raw_table_partition_count_query)
    raw_table_count = raw_result_df["total"].tolist()
    print(raw_table_count)

    temp_result_df = hook.get_pandas_df(temp_table_count_query)
    temp_table_count = temp_result_df["total"].tolist()
    print(temp_table_count)

    if raw_result_df.equals(temp_result_df):
        print("\tCount Matches in both Raw and Temp tables")
        return "delete_temp_table"
    else:
        message = f"""{dag_id} | {project_id} | {dataset_id} | {raw_table_id} | {temp_table_id} | Data count mismatch identified | {raw_table_count=} | {temp_table_count=}"""
        ti.xcom_push(key="slack_message", value=message)
        raise AirflowException(message)


# -----------------------------------------------------------------------------
# DAG Tasks
# -----------------------------------------------------------------------------

set_xcom_variables_task = PythonOperator(
    task_id="set_xcom_variables",
    python_callable=set_xcom_variables,
    provide_context=True,
    dag=dag,
)

create_temp_table_task = GCSToBigQueryOperator(
    task_id="create_temp_table",
    bucket=gcs_bucket,
    source_objects=['{{ ti.xcom_pull(key="gcs_prefix") }}'],
    destination_project_dataset_table='{{ ti.xcom_pull(key="temp_table_uri") }}',
    source_format=gcs_file_format,
    write_disposition="WRITE_TRUNCATE",
    encoding="UTF-8",
    external_table=True,
    autodetect=True,
    project_id=project_id,
    labels=labels,
    dag=dag,
)


delete_partition_if_exists_task = BigQueryInsertJobOperator(
    task_id="delete_partition_if_exists",
    configuration={
        "query": {
            "query": '{{ ti.xcom_pull(key="delete_partition_from_table_query") }}',
            "useLegacySql": False,
        }
    },
    dag=dag,
)

insert_into_raw_table_task = BigQueryInsertJobOperator(
    task_id="insert_into_raw_table",
    configuration={
        "query": {
            "query": '{{ ti.xcom_pull(key="insert_into_table_query") }}',
            "useLegacySql": False,
        }
    },
    dag=dag,
)


delete_temp_table_task = BigQueryDeleteTableOperator(
    task_id="delete_temp_table",
    deletion_dataset_table='{{ ti.xcom_pull(key="temp_table_uri") }}',
    ignore_if_missing=False,
    dag=dag,
)


delete_temp_table_if_exists_task = BigQueryDeleteTableOperator(
    task_id="delete_temp_table_if_exists",
    deletion_dataset_table='{{ ti.xcom_pull(key="temp_table_uri") }}',
    ignore_if_missing=True,
    dag=dag,
)


validate_schema_task = BranchPythonOperator(
    task_id="validate_schema",
    python_callable=validate_schema,
    provide_context=True,
    dag=dag,
)

validate_data_count_task = BranchPythonOperator(
    task_id="validate_data_count",
    python_callable=validate_data_count,
    provide_context=True,
    dag=dag,
)

send_alert_task = SlackAPIPostOperator(
    task_id="send_alert",
    text="{{ task_instance.xcom_pull(key='slack_message') }}",
    channel=slack_channel_id,
    username=slack_username,
    trigger_rule="one_failed",
    dag=dag,
)


# -----------------------------------------------------------------------------
# DAG's Tasks Dependencies (ie execution order)
# -----------------------------------------------------------------------------


(
    set_xcom_variables_task
    >> delete_temp_table_if_exists_task
    >> delete_partition_if_exists_task
    >> create_temp_table_task
    >> validate_schema_task
    >> [insert_into_raw_table_task, send_alert_task]
)

(
    insert_into_raw_table_task
    >> validate_data_count_task
    >> [delete_temp_table_task, send_alert_task]
)


send_alert_task
