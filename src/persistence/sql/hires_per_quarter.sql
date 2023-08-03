with employees_by_quarter as (
	select
	department_id,
	job_id,
	case
		when extract(month from datetime) between 1 and 3 then 1
		when extract(month from datetime) between 4 and 6 then 2
		when extract(month from datetime) between 7 and 9 then 3
		else 4
	end as quarter
	from hired_employees
	where extract(year from datetime) = 2021
),
q1_employees as (
	select department_id, job_id, count(*) as total_employees
	from employees_by_quarter
	where quarter = 1
	group by department_id, job_id
),
q2_employees as (
	select department_id, job_id, count(*) as total_employees
	from employees_by_quarter
	where quarter = 2
	group by department_id, job_id
),
q3_employees as (
	select department_id, job_id, count(*) as total_employees
	from employees_by_quarter
	where quarter = 3
	group by department_id, job_id
),
q4_employees as (
	select department_id, job_id, count(*) as total_employees
	from employees_by_quarter
	where quarter = 4
	group by department_id, job_id
),
departments_and_jobs as (
	select distinct department_id, job_id
	from hired_employees
)
select distinct 
	d.department,
	j.job,
	coalesce(q1_employees.total_employees, 0) as q1,
	coalesce(q2_employees.total_employees, 0) as q2,
	coalesce(q3_employees.total_employees, 0) as q3,
	coalesce(q4_employees.total_employees, 0) as q4
from departments_and_jobs he
inner join departments d on he.department_id = d.id
inner join jobs j on he.job_id = j.id
left join q1_employees on he.department_id = q1_employees.department_id and he.job_id = q1_employees.job_id
left join q2_employees on he.department_id = q2_employees.department_id and he.job_id = q2_employees.job_id
left join q3_employees on he.department_id = q3_employees.department_id and he.job_id = q3_employees.job_id
left join q4_employees on he.department_id = q4_employees.department_id and he.job_id = q4_employees.job_id
order by d.department, j.job