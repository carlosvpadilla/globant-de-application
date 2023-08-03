with hires_per_department as (
	select department_id, count(*) as number_of_hires
	from hired_employees
	where extract(year from datetime) = 2021
	group by department_id
),
mean_of_hires as (
	select avg(number_of_hires) as mean
	from hires_per_department
)
select hd.department_id as id, d.department, hd.number_of_hires as hired
from hires_per_department hd
inner join departments d on hd.department_id = d.id
where number_of_hires > (
	select mean from mean_of_hires
)
order by number_of_hires desc