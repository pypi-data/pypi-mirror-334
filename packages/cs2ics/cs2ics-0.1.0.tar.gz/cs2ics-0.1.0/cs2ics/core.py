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
    def event_title(self) -> str:
        return f"{self.name} - {self.classroom}"

    @property
    def event_description(self) -> str:
        return f"教师: {self.teacher}"


@dataclass
class CourseSchedule:
    timetable: List[Tuple[int, int]]
    start_date: Tuple[int, int, int]
    courses: List[Course]
    duration: int = 45

    ICAL_HEADER = [
        "BEGIN:VCALENDAR",
        "METHOD:PUBLISH",
        "VERSION:2.0",
        "X-WR-CALNAME:课程表",
        "X-WR-TIMEZONE:Asia/Shanghai",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Shanghai",
        "END:VTIMEZONE",
    ]
    ICAL_FOOTER = ["END:VCALENDAR"]

    def __post_init__(self):
        self._validate_inputs()
        self.timetable.insert(0, (0, 0))  # 占位索引0
        self._base_date = self._calculate_base_date()

    def _validate_inputs(self):
        if not self.timetable:
            raise ScheduleError("必须设置课程时间表")
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
            f"SUMMARY:{course.event_title}",
            f"DESCRIPTION:{course.event_description}",
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
