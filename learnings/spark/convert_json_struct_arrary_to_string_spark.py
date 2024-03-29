import spark.implicits._
from pyspark.sql.functions import *


jsonStrings =  ["""
  {
    "name": "Yin",
    "DOB": "05-11-1989",
    "Edu": {"S": "Masters", "L": "Cyber Security"},
    "city": {"S": "Columbus"},
    "state": {"S": "Ohio"},
    "number0": {"L": [{"S": "One"}, {"S": "Two"}, {"S": "Three"}]},
    "number1": {"S": "Text", "L": [{"S": "One"}, {"S": "Two"}, {"S": "Three"}]}
  }
  """]

otherPeopleRDD = sc.parallelize(jsonStrings)

df = spark.read.json(otherPeopleRDD)
df.show()

_df = df
print(_df.dtypes)
non_struct_cols = [c[0] for c in _df.dtypes if c[1][:6] != 'struct']
print("non_struct_cols - ", non_struct_cols)
struct_cols = [c[0] for c in _df.dtypes if c[1][:6] == 'struct']
print('struct_cols - ', struct_cols)
parsed_cols = []
for _col in struct_cols:
    string_list = []
    array_list = []
    print(f'[*] {_col}')
    flat_cols = list(_df.select(_col + '.*').columns)
    for _key in flat_cols:
        print(f'[*] {_col}.{_key}', _df.select(f'{_col}.{_key}').dtypes)
        if _df.select(f'{_col}.{_key}').dtypes[0][1][:6] in ['string']:
            string_list.append(f'{_col}.{_key}')
        elif _df.select(f'{_col}.{_key}').dtypes[0][1][:5] in ['array']:
            for x in df.select(explode(f'{_col}.{_key}').alias('tmp')).select('tmp.*').columns:
                array_list.append(f'{_col}.{_key}.{x}')
    if not array_list and string_list:
        _df = _df.withColumn(_col, concat_ws('-', *string_list))
        parsed_cols.append(_col)
    elif array_list and not string_list:
        if len(array_list) == 1:
            _df = _df.withColumn(_col, concat_ws('-', *array_list))
            parsed_cols.append(_col)
    elif array_list and string_list:
        if len(array_list) == 1:
            _df = _df.withColumn(_col+'_tmp', concat_ws(',', *array_list))
            string_list.append(_col+'_tmp')
            _df = _df.withColumn(_col, concat_ws('-', *string_list))
            parsed_cols.append(_col)


_df.select(non_struct_cols + parsed_cols).show(50, False)
