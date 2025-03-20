from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import md5
from typing import List, Tuple
from .exception import ScheduleError

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
        return f"{self.name} - {self.location}-{self.classroom}"

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

    def __post_init__(self):
        self._validate_inputs()
        self.timetable.insert(0, (0, 0))    # 在时间表的第一项插入(0, 0)以便索引与课程索引对齐
        self._base_date = self._calculate_base_date()

    def _validate_inputs(self):
        if len(self.start_date) != 3:
            raise ScheduleError("开学日期格式应为(年, 月, 日)")
        if not self.courses:
            raise ScheduleError("至少需要一门课程")

    def _calculate_base_date(self) -> datetime:
        """计算学期第一个周一"""
        dt = datetime(*self.start_date)
        return dt - timedelta(days=dt.weekday())

    def generate_ical(self) -> str:
        """生成iCalendar内容"""
        events = []
        runtime = datetime.utcnow()

        for course in self.courses:
            for week in course.weeks:
                event = self._build_event(course, week, runtime)
                events.extend(event)

        return self._format_ical(events)

    def _build_event(self, course: Course, week: int, runtime: datetime) -> List[str]:
        """构建单个课程事件"""
        start = self._calculate_time(week, course.weekday, course.indexes[0])
        end = self._calculate_time(
            week, course.weekday, course.indexes[-1], add_duration=True
        )

        return [
            "BEGIN:VEVENT",
            f"SUMMARY:{course.get_course_title}",
            f"DESCRIPTION:{course.get_course_description}",
            f"DTSTART;TZID=Asia/Shanghai:{start:%Y%m%dT%H%M%S}",
            f"DTEND;TZID=Asia/Shanghai:{end:%Y%m%dT%H%M%S}",
            f"DTSTAMP:{runtime:%Y%m%dT%H%M%SZ}",
            f"UID:{self._generate_uid(course, week)}",
            f"LOCATION:{course.location}",
            "END:VEVENT",
        ]

    def _calculate_time(
        self, week: int, weekday: int, index: int, add_duration: bool = False
    ) -> datetime:
        """计算具体时间"""
        date = self._base_date + timedelta(weeks=week - 1, days=weekday - 1)
        hour, minute = self.timetable[index]
        if add_duration:
            return date.replace(hour=hour, minute=minute) + timedelta(
                minutes=self.duration
            )
        return date.replace(hour=hour, minute=minute)

    @staticmethod
    def _generate_uid(course: Course, week: int) -> str:
        """生成唯一事件ID"""
        seed = (
            f"{course.name}-{course.teacher}-{week}-{course.weekday}-{course.indexes}"
        )
        return md5(seed.encode()).hexdigest()

    def _format_ical(self, events: List[str]) -> str:
        """格式化iCalendar内容"""
        lines = []
        for line in self.ICAL_HEADER + events + self.ICAL_FOOTER:
            while len(line) > 72:
                lines.append(line[:72])
                line = " " + line[72:]
            lines.append(line)
        return "\n".join(lines)
