```bash
pip install runqdm
```

## What is runqdm?

runqdm visually represents the progress of your **running** code with a **running** person ASCII animation

## Usage Examples

```python
from runqdm import runqdm

for i in runqdm(range(10)):
    sum(x ** 2 for x in range(1, 10**7))  
```
```python
from runqdm import runqdm
import time

for i in runqdm([1,2,3,4,5]):
    time.sleep(2)
```
