import os
import subprocess
import certifi
import asyncio
import aiofiles
import aiohttp
import json
import dotenv
import time
import ssl
import random
import json
import uvloop
import random
import argparse

from datetime import datetime
from google.cloud import bigquery

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())
tcpconn = aiohttp.TCPConnector(ssl=ssl_context)

dotenv.load_dotenv()
current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%Y-%m-%d")
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

root_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(root_dir, "data")
sql_dir = os.path.join(root_dir, "bigquery")

os.environ['SSL_CERT_FILE'] = certifi.where()

host = os.environ["APIC__HOSTNAME"]
username = os.environ["APIC__USERNAME"]
password = os.environ["APIC__PASSWORD"]
host_url = f"https://{host}/api/v2"
signin_url = f"{host_url}/authentication/signin"
signin_data = json.dumps({"name": username, "password": password})
max_retry = 2

gcp_cloud_storage_dir = os.environ["GOOGLE_CLOUD_STORAGE"] 
gcp_bigquery_dataset = os.environ["GOOGLE_CLOUD_DATASET"]
gcp_project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def create_dir(path: str) -> None:
    try:
        os.makedirs(path)
    except:
        pass


def read_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.read()
    

async def write_response_as_json(data, output_file):
    async with aiofiles.open(output_file, "w", encoding="utf-8") as f:
        await f.write(data)
        await asyncio.sleep(0)


async def fetch(session, semaphore, fetch_url,  params, retry=0):
    try:
        async with semaphore:
            async with session.get(fetch_url, params=params) as response:
                await asyncio.sleep(1)
                if response.status != 200:
                    print(f"{response.headers.get('DATE')}:{response.url} - {response.status}")
                if response.status > 399:
                    response.raise_for_status()
                data = await response.json()
                await asyncio.sleep(1)
                return data
    except aiohttp.client_exceptions.ClientOSError as e:
        if retry < max_retry:
            await asyncio.sleep(2 + random.randint(1,10))
            data = await fetch(session, semaphore, fetch_url,  params, retry=retry+1)
            await asyncio.sleep(1)
            return data
        else:
            print(f'Retry failed! {fetch_url} - {retry=}')
            return {}
    except Exception as e:
        print(str(e))
        return {}


async def request_api(session, semaphore, fetch_url, params, output_file):

    data = await fetch(session, semaphore, fetch_url, params)
    await asyncio.sleep(1)

    if isinstance(data, dict) and len(data.get("content", [])):
        delimited_json = "\n".join(
                                [json.dumps({'extracted_dt': formatted_datetime, **x}) 
                                for x in data["content"]])
        await write_response_as_json(delimited_json, output_file)
        await asyncio.sleep(1)

        if all(key in list(data.keys()) for key in ['pageNumber', 'totalPages']) and data.get('totalPages', 0) > 1 :
            new_page_number = data['pageNumber'] + 1
            if new_page_number < data['totalPages']:
                new_output_file = output_file.replace(f'{params["page"]}.json', f'{new_page_number}.json')
                new_params = params.copy()
                new_params['page'] = new_page_number
                task = asyncio.create_task(request_api(session, semaphore, fetch_url, new_params, new_output_file))
                await task
                await asyncio.sleep(1)
    else:
        print(f'No data found! - {fetch_url} - {params} - {data}')


async def main(kwargs_list):
    semaphore = asyncio.Semaphore(1000)

    async with aiohttp.ClientSession() as session:
        session.headers.update({"accept": "application/json", "content-type": "application/json"})

        async with session.post(signin_url, data=signin_data, ssl_context=ssl_context) as response:
            if response.status > 399:
                response.raise_for_status()
            data = await response.json()
        session.headers.update({"X-AUTH-TOKEN": data["token"]})

        # print(session.headers)
        coros = [request_api(session=session, semaphore=semaphore, **kwargs) for kwargs in kwargs_list]
        await asyncio.gather(*coros)


def run_subprocess(cmd):
    print(" ".join(cmd))
    result = subprocess.run(cmd,check=True,capture_output=True, text=True)
    print("Return code:", result.returncode)
    if result.stdout:
        print("Standard output:", result.stdout)
    # if result.stderr:
    #     print("Standard error:", result.stderr)
    return result.stdout


def run_bigquery_sql_to_df(query=''):
    if not query:
        return []
    client = bigquery.Client(project=gcp_project_id)
    return client.query(query).to_dataframe()


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("slug", type=str, choices=['xxxx', 'yyyy'])
    args=parser.parse_args()
    
    slug = args.slug
    output_dir = os.path.join(data_dir, slug, formatted_date)
    create_dir(output_dir)

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    if slug == 'yyyy':
        df = run_bigquery_sql_to_df(mappings[slug]['query'])
        batch_size = mappings[slug]['batch_size']
        df['device_ids'] = df['device_id'].astype(int)
        device_ids = df['device_id'].tolist()
        print(f'Total device ids - {len(device_ids)}')

        # Loop through device ids in batches
        for i in range(0,len(device_ids), batch_size):
            _kwargs = [{'fetch_url':mappings[slug]['fetch_url'].format(_id), 
                        'params':mappings[slug]['params'], 
                        'output_file': os.path.join(output_dir, mappings[slug]['output_file'].format(_id))} 
                        for _id in device_ids[i:i+batch_size] 
                        if not os.path.isfile(
                            os.path.join(output_dir, mappings[slug]['output_file'].format(_id)))]
            
            start = time.time()
            asyncio.get_event_loop().run_until_complete(main(_kwargs))
            pending_calls = len(device_ids) - (i+batch_size)
            print(f"# Time to complete '{slug}': {round(time.time() - start, 2)} seconds..")
            print(datetime.now(), "---------------->>>>>>>>>>>>>>>", i, i+batch_size, pending_calls)

    elif slug in ('xxxx'):
        _kwargs = [{ 'fetch_url':mappings[slug]['fetch_url'], 
                    'params':mappings[slug]['params'], 
                    'output_file': os.path.join(output_dir, mappings[slug]['output_file'])}]
            
        start = time.time()
        asyncio.get_event_loop().run_until_complete(main(_kwargs))
        print(f"# Time to complete '{slug}': {round(time.time() - start, 2)} seconds..")
        print("---------------->>>>>>>>>>>>>>>", datetime.now())

    print("# Local to GCP Cloud Storage")
    run_subprocess(['gsutil', '-m', 'cp', '-R', output_dir, f'gs://{gcp_cloud_storage_dir}/{slug}/'])
    # run_subprocess(['gsutil', '-m', 'rsync', '-r', output_dir, f'gs://{gcp_cloud_storage_dir}/{slug}/'])

    print('# Delete old bigquery raw table if exists already')
    run_subprocess(['bq', 'rm', '-f', '-t', f'{gcp_bigquery_dataset}.raw_{slug}_{formatted_date}'])

    print('# Create a new bigquery raw table from the latest json files')
    run_subprocess(['bq', 'load', '--autodetect', '--source_format=NEWLINE_DELIMITED_JSON', f'{gcp_bigquery_dataset}.raw_{slug}_{formatted_date}', f"gs://{gcp_cloud_storage_dir}/{slug}/{formatted_date}/{slug}_*.json"])

    print('# Delete old bigquery stage table if exists already')
    run_subprocess(['bq', 'rm', '-f', '-t', f'{gcp_bigquery_dataset}.stage_{slug}'])

    print('# Create stage table from raw table')
    stage_sql = read_file(os.path.join(sql_dir, mappings[slug]['stage_table']))
    stage_sql = stage_sql.format(formatted_date=formatted_date).replace('\n', ' ')
    run_subprocess(['bq',  'query', '--batch', '--use_legacy_sql=false',  f'{stage_sql}'])
    
    print(' # Run merge stage table with final table query')
    merge_query = read_file(os.path.join(sql_dir, mappings[slug]['merge_query']))
    run_subprocess(['bq',  'query', '--batch', '--use_legacy_sql=false',  f'{merge_query}'])

    print('# Delete old bigquery raw table if exists already')
    run_subprocess(['bq', 'rm', '-f', '-t', f'{gcp_bigquery_dataset}.raw_{slug}_{formatted_date}'])

    # print('# Delete local files')
    # # ToDO
