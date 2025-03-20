# CS2ICS

这是一个用于将课程表转换为 ics 格式日历文件的工具

## 用法

### 实例化课程

对于课程的定义，它应该有以下属性

```python
@dataclass
class Course:
    name: str
    teacher: str
    classroom: str
    location: str
    weekday: int
    weeks: List[int]
    indexes: List[int]

    @property
    def get_course_title(self) -> str:
        return f"{self.name} - {self.classroom}"

    @property
    def get_course_description(self) -> str:
        return f"教师: {self.teacher}"
    
    @property
    def get_course_location(self) -> str:
        return self.location
    
    @property
    def get_course_weekday(self) -> int:
        return self.weekday
    
    @property
    def get_course_weeks(self) -> List[int]:
        return self.weeks
    
    @property
    def get_course_indexes(self) -> List[int]:
        return self.indexes
    
    @property
    def get_course_name(self) -> str:
        return self.name
    
    @property
    def get_course_teacher(self) -> str:
        return self.teacher
    
    @property
    def get_course_classroom(self) -> str:
        return self.classroom

```

在实例化的过程中，你需要传入

```python
name: str
teacher: str
classroom: str
location: str
weekday: int
weeks: List[int]
indexes: List[int]
```

他们分别代表了

- `name`: 课程名称
- `teacher`: 课程授课老师
- `classroom`: 课程上课教室
- `location`: 课程上课地点
- `weekday`: 课程上课的日子（表示周几）
- `weeks`: 课程上课的周次（第几周上这门课）
- `indexes`: 课程上课的节次（关系到上课时间）

在这里有这样的一个例子

```python
math_course = Course(
        name="高等数学",
        teacher="朱老师",
        classroom="201",
        location="教学三号楼",
        weekday=1,
        weeks=weeks_range(1, 18),
        indexes=[1, 2],
)
```

在这里实例化了高数课，我认为你需要重点关注 `weeks` 的传入值

在这里，我使用了 `weeks_range` 函数（它在 `cs2ics.utils` 里面），来生成一个包含 1~18 周的列表，同样的，你还可以引入 `odd_weeks` 和 `even_weeks` 来生成奇数周和偶数周的列表

### 实例化课程表

对于课程表，有如下定义

```python
@dataclass
class CourseSchedule:
    start_date: Tuple[int, int, int]
    courses: List[Course]
    duration: int = 45
    timetable = [   # 需要修改的话，请在实例化 CourseSchedule 实例化时传入你的时间表
        (8, 30), # 上午第一节课时间为 8:30 至 9:15
        (9, 20), # 上午第二节课时间为 9:20 至 10:05
        (10, 25), # 上午第三节课时间为 10:25 至 11:10
        (11, 15), # 上午第四节课时间为 11:15 至 12:00
        (13, 50), # 下午第一节课时间为 13:50 至 14:35
        (14, 40), # 下午第二节课时间为 14:40 至 15:25 
        (15, 30), # 下午第三节课时间为 15:30 至 16:15
        (16, 30), # 下午第四节课时间为 16:30 至 17:15
        (17, 20), # 下午第五节课时间为 17:20 至 18:05
        (18, 30), # 晚上第一节课时间为 18:30 至 19:15
        (19, 20), # 晚上第二节课时间为 19:20 至 20:05
        (20, 10), # 晚上第三节课时间为 20:10 至 20:55
    ]
    timezone = "Asia/Shanghai"
    ICAL_HEADER = [
        "BEGIN:VCALENDAR",
        "METHOD:PUBLISH",
        "VERSION:2.0",
        "X-WR-CALNAME:课程表",
        f"X-WR-TIMEZONE:{timezone}",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        f"TZID:{timezone}",
        "END:VTIMEZONE",
    ]
    ICAL_FOOTER = ["END:VCALENDAR"]
```

你需要关注课程表实例化中的部分变量，分别是

- `start_date`: 表示开学日期
- `courses`: 是一个包含 `Course` 类型实例变量的列表
- `duration`: 时长，表示一节课上多久
- `timetable`: 上课时间表，这里是每节课上课的时间，结束的时间会根据你提供的时长进行计算
- `timezome`: 时区，默认为 `Asia/Shanghai`

下面是创建一个课程表的示例代码

```python
courses = [
    Course(
        name="形势与政策",
        teacher="李卫华",
        classroom="教3-304",
        location="教3-304",
        weekday=1,
        weeks=[11, 12],
        indexes=[1, 2],
    ),
    Course(
        name="大学物理(1)",
        teacher="刘慧",
        classroom="教1-325",
        location="教1-325",
        weekday=3,
        weeks=weeks_range(1, 18),
        indexes=[1, 2],
    ),
]

calendar = CourseSchedule(
    start_date=(2024, 2, 24),   # 开学日期
    courses=courses,
)
```

这里实例化了一个 `calendar` 变量，为 `CourseSchedule` 类型（即课程表）

### 生成课表并保存到文件

`CourseSchedule` 类型变量拥有名为 `generate_ical` 的函数，这个函数的定义如下

```python
class CourseSchedule:
    # ...
    
    def generate_ical(self) -> str:
        """生成iCalendar内容"""
        events = []
        runtime = datetime.utcnow()

        for course in self.courses:
            for week in course.weeks:
                event = self._build_event(course, week, runtime)
                events.extend(event)

        return self._format_ical(events)
    
    def _format_ical(self, events: List[str]) -> str:
        """格式化iCalendar内容"""
        lines = []
        for line in self.ICAL_HEADER + events + self.ICAL_FOOTER:
            while len(line) > 72:
                lines.append(line[:72])
                line = " " + line[72:]
            lines.append(line)
        return "\n".join(lines)
    
	# ...
```

所以只需要调用 `generate_ical` 函数并保存到文件即可

```python
with open("test_schedule.ics", "w", encoding="utf-8") as f:
    f.write(calendar.generate_ical())
```

这样就会把课程表保存到 `test_schedule.ics` 文件

