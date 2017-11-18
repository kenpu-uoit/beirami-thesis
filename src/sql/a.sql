SELECT * FROM
(select 
 r_id,
 first_value(c) over w as c,
 first_value(deleted) over w as del,
 (max(op_id) over w) - (min(op_id) over w) + 1 as freq
from tl where op_id > 1001
WINDOW w AS (partition by r_id order by op_id desc)) T
where del = false
limit 10;

