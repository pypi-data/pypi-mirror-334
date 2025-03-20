# Welcome

It's Monolith, a code execution environment. You can run code in a variety of languages, and see the output.

Should you have any questions, please don't hesitate to ask mingzhe@nus.edu.sg.


```python
from monolith import monolith

monolith = monolith.Monolith(backend_url='https://monolith.cool')

post_response = monolith.post_code_submit(
    lang = 'python3',
    libs = [],
    code = 'print("Hello, World!")',
    timeout = 10,
    profiling = False
)

task_id = post_response['task_id']

get_response = monolith.get_code_result(task_id)
print(get_response)
```