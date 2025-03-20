import time
from dataclasses import dataclass


@dataclass
class TimerSegment:
    name: str = ""
    start_time: float = 0.0
    stop_time: float = 0.0
    duration: float = 0.0


class Timer:
    def __init__(
        self,
    ):
        self._segments = []
        self._current_segment = None

    @property
    def segments(
        self,
    ) -> list[TimerSegment]:
        return self._segments

    def reset(
        self,
    ):
        self._segments = []
        self._current_segment = None

    def start(
        self,
        segment_name: str,
    ):
        if self._current_segment:
            current_time = time.time()
            segment = TimerSegment(
                name=self._current_segment.name,
                start_time=self._current_segment.start_time,
                stop_time=current_time,
                duration=current_time - self._current_segment.start_time,
            )
            self._segments.append(segment)
            self._current_segment = TimerSegment(
                name=segment_name,
                start_time=current_time,
            )
        else:
            current_time = time.time()
            self._current_segment = TimerSegment(
                name=segment_name,
                start_time=current_time,
            )

    def split(
        self,
        name: str,
    ):
        assert self._current_segment
        current_time = time.time()
        segment = TimerSegment(
            name=name,
            start_time=self._current_segment.start_time,
            stop_time=current_time,
            duration=current_time - self._current_segment.start_time,
        )
        self._segments.append(segment)

    def stop(
        self,
    ):
        if self._current_segment:
            current_time = time.time()
            segment = TimerSegment(
                name=self._current_segment.name,
                start_time=self._current_segment.start_time,
                stop_time=current_time,
                duration=current_time - self._current_segment.start_time,
            )
            self._segments.append(segment)
            self._current_segment = None
