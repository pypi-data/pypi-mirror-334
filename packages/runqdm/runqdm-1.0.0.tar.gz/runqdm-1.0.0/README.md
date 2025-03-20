# runqdm

애니메이션이 있는 진행 상태 표시줄 패키지입니다. 실행 중인 사람 애니메이션과 함께 진행 상황을 시각적으로 보여줍니다.

## 설치

```bash
pip install runqdm
```

## 사용법

```python
from runqdm import runqdm
import time

# 반복 가능한 객체와 함께 사용
for i in runqdm(range(100)):
    # 시간이 걸리는 작업 수행
    time.sleep(0.1)

# 리스트와 함께 사용
for item in runqdm(['a', 'b', 'c', 'd']):
    # 작업 수행
    time.sleep(0.5)
```

## 특징

- 실행 중인 사람 ASCII 아트 애니메이션
- 진행률 표시 (퍼센트, 진행 막대)
- 현재/전체 항목 수 표시
- 남은 시간 예상 (hh:mm:ss 형식)

## 요구 사항

- Python 3.6 이상
- setuptools
- colorama (Windows에서 ANSI 색상 지원)

## 라이선스

MIT 라이선스 