set
schema 'temp';

select  
	to_char(current_date , 'YYYY')::int,
	to_char(current_date, 'MM')::int,
	to_char(current_date, 'DD')::int,
	to_char(current_date, 'day')::varchar,
	to_char(current_date + '1 day'::interval, 'YYYY-MM-DD')::date;

select to_char(current_date - interval '6 months', 'YYYY-MM-DD'):: date;
select to_char(current_date - interval '30 days', 'YYYY-MM-DD'):: date;

select
	date::date
from
	generate_series(
	'2022-01-24'::date, --START date
	'2022-07-26'::date, -- END date
	'15 days'::interval) date
/*
2022-01-26
2022-02-10
2022-02-25
2022-03-12
2022-03-27
2022-04-11
2022-04-26
2022-05-11
2022-05-26
2022-06-10
2022-06-25
2022-07-10
2022-07-25
*/
	
	
select
	*,
	lead(s.day1) over(
	order by day1) as next_day
from
	(
	select
		to_char(to_date('2022-01-26', 'YYYY-MM-DD') + interval '15 days', 'YYYY-MM-DD')::date day1) s
;

select
	to_char(to_date('2022-01-26', 'YYYY-MM-DD') + interval '15 days', 'YYYY-MM-DD')::date 

select
	to_char('2022-01-26'::date + interval '15 days', 'YYYY-MM-DD')::date 