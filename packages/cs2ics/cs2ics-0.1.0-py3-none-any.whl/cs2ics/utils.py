from typing import List

def even_weeks(start: int, end: int) -> List[int]:
    """生成偶数周列表"""
    return [w for w in range(start, end + 1) if w % 2 == 0]


def odd_weeks(start: int, end: int) -> List[int]:
    """生成奇数周列表"""
    return [w for w in range(start, end + 1) if w % 2 != 0]


def weeks_range(start: int, end: int) -> List[int]:
    """生成连续周列表"""
    return list(range(start, end + 1))