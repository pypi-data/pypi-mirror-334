import datetime
from datetime import timedelta

# Константы, определяющие границы Python-даты (year=1..9999).
DT_MIN = datetime.datetime.min  # 0001-01-01 00:00:00
DT_MAX = datetime.datetime.max  # 9999-12-31 23:59:59.999999
EPOCH_RANGE = DT_MAX - DT_MIN  # Разница (timedelta) между min и max


class ExtendedPartialDateTime:
    def __init__(self,
                 year=None, month=None, day=None,
                 hour=None, minute=None, second=None, microsecond=None,
                 relative_offset=timedelta(0),
                 weekday: int = None,  # 0 - понедельник, 6 - воскресенье
                 epoch_shift: int = 0):
        """
        year, month, day, hour, minute, second, microsecond -- «сырые» поля даты (могут выходить за 1..9999).
        relative_offset -- дополнительное смещение по времени (timedelta).
        weekday -- хранится для информации (если известно).
        epoch_shift -- на сколько "эпох" мы сдвинулись от базового интервала [DT_MIN..DT_MAX].
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

        self.relative_offset = relative_offset
        self._weekday = weekday

        # Сколько раз мы "пролистали" весь диапазон [1..9999], если вышли за него
        self.epoch_shift = epoch_shift

        # Если год, месяц и день заданы, но weekday не задан, вычислим автоматически
        if (year is not None and month is not None and day is not None and weekday is None):
            try:
                base_wd = datetime.datetime(year, month, day).weekday()
                offset_days = int(relative_offset.total_seconds() // 86400)
                self._weekday = (base_wd + offset_days) % 7
            except ValueError:
                # Может быть ошибка, если год < 1 или > 9999. Игнорируем здесь.
                pass

    @property
    def weekday(self):
        return self._weekday

    @weekday.setter
    def weekday(self, value):
        self._weekday = value

    def is_complete(self):
        """
        Проверяем, что заполнены все компоненты (год, месяц, день, час, мин, сек, микросекунды).
        """
        return None not in (
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond
        )

    def to_datetime_simple(self) -> datetime.datetime:
        """
        Простой метод: пытается напрямую создать datetime( year, month, day ... ).
        Упадёт с ValueError, если год < 1 или год > 9999.
        Не учитывает epoch_shift!
        """
        if not self.is_complete():
            raise ValueError("Невозможно преобразовать в datetime, не все поля заданы.")
        dt = datetime.datetime(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond
        )
        return dt + self.relative_offset

    def to_extended_datetime(self) -> datetime.datetime:
        """
        Расширенный метод, который учитывает:
         1) Год может быть < 1 или > 9999: тогда мы «прокручиваем» epoch_shift,
            пока год не влезет в [1..9999].
         2) Если после смещения всё равно выходит за границы,
            продолжаем сдвигать epoch_shift на ±1, пока не попадём в допустимый диапазон.
         3) В итоге возвращаем «обычный» datetime в пределах year=1..9999.
        """
        if not self.is_complete():
            raise ValueError("Невозможно преобразовать в datetime, не все поля заданы.")

        # 1. Соберём «сырой» год/месяц/день (которые могут выходить за 1..9999).
        raw_year = self.year
        raw_month = self.month
        raw_day = self.day
        raw_hour = self.hour
        raw_minute = self.minute
        raw_second = self.second
        raw_microsecond = self.microsecond

        # 2. Пока год не влезает в [1..9999], будем смещать epoch_shift на ±1,
        #    и прибавлять/вычитать длину диапазона в годах.
        #    Но поскольку «размер» одного полного цикла — это EPOCH_RANGE (timedelta),
        #    придётся аккуратно вычислять, на сколько лет сдвигать.
        #
        #    Упрощённый подход: заодно напрямую создадим datetime с clamp (зажатием) —
        #    если raw_year < 1, мы будем уходить в предыдущую эпоху,
        #    если raw_year > 9999, уходим в следующую эпоху.
        #    Повторяем, пока не попадём внутрь.
        #
        #    ВНИМАНИЕ: просто складывать/вычитать 9999 недостаточно,
        #    ведь точное количество дней зависит от високосов.
        #    Поэтому «смещать» нужно именно в timedelta. Для этого сначала создадим "пробный" dt
        #    в корневом диапазоне (зажимая его в [1..9999] по году). А затем посмотрим,
        #    на сколько дней он отличается от «сырых» данных.

        # Шаг 2а. Пробуем сначала "зажать" год в границы 1..9999 для временного dt:
        def clamp_year(y: int) -> int:
            """Зажимаем год в диапазон [1..9999]."""
            return max(1, min(y, 9999))

        # Сформируем "пробный" год, зажатый в [1..9999]
        clamped_year = clamp_year(raw_year)

        # Пробуем создать datetime (могут быть кривые month/day, если raw_month=13 и т.д.),
        # но предположим, что month и day валидны (1..12 и 1..31, проверку можно добавить).
        try:
            test_local_dt = datetime.datetime(
                clamped_year,
                raw_month,
                raw_day,
                raw_hour,
                raw_minute,
                raw_second,
                raw_microsecond
            )
        except ValueError:
            # Могут быть месяцы/дни вне диапазона.
            # Для упрощённого примера не будем это подробно обрабатывать,
            # но при необходимости здесь можно «докручивать» месяц/день.
            raise ValueError("Невозможно создать 'локальный' datetime из указанных полей")

        # Теперь хотим узнать, как далеко (по дням/секундам) находится test_local_dt
        # от «сырых» данных (raw_year, raw_month...), если бы они не были ограничены 1..9999.
        # Но Python не позволяет сделать datetime с year < 1 или > 9999 напрямую,
        # поэтому «сырые» координаты нельзя сразу создать через datetime.
        #
        # Мы можем «разницу» учесть через количество "эпох" (EPOCH_RANGE).
        # Идея: если raw_year < 1, то test_local_dt будет сильно «правее»,
        #       значит нужно уменьшать epoch_shift.
        # Если raw_year > 9999, наоборот, увеличивать epoch_shift.
        #
        # Но лучше всего поступить итеративно:
        #   Пока test_local_dt < DT_MIN, делаем epoch_shift -= 1
        #   Пока test_local_dt > DT_MAX, делаем epoch_shift += 1
        #
        # А потом снова пересчитываем test_local_dt (потому что локальная дата
        # фактически сдвинулась на ± EPOCH_RANGE).

        # Начнём test_local_dt как есть:
        local_dt = test_local_dt

        # Применим relative_offset сразу же:
        local_dt += self.relative_offset

        # Учтём уже текущий self.epoch_shift (вдруг он не 0)
        # Для этого добавим к local_dt: epoch_shift * EPOCH_RANGE
        # (если epoch_shift отрицательный, будет вычитание)
        shift_delta = self.epoch_shift * EPOCH_RANGE
        local_dt += shift_delta

        # Теперь смотрим, вышли ли мы за пределы [DT_MIN..DT_MAX].
        # Если да, то надо сдвинуться на ±1 эпоку, пока не попадём внутрь.
        while local_dt < DT_MIN:
            self.epoch_shift -= 1
            local_dt += EPOCH_RANGE  # смещаем дату в диапазон
        while local_dt > DT_MAX:
            self.epoch_shift += 1
            local_dt -= EPOCH_RANGE

        # После такого цикла local_dt гарантированно в диапазоне [DT_MIN..DT_MAX].
        # Это и будет наш "расширенный" datetime.
        return local_dt

    @classmethod
    def from_extended_datetime(cls, dt: datetime.datetime) -> 'PartialDateTime':
        """
        Обратная операция: если мы уже имеем реальный datetime в диапазоне [1..9999],
        но с учётом «виртуального» сдвига (epoch_shift), то на практике dt может быть
        любым (например, user мог хранить бесконечную дату и при to_extended_datetime()
        получить dt внутри 1..9999).

        Однако, если dt фактически уже в пределах 1..9999, мы можем напрямую выдернуть year..microsecond.
        Если хотим понять, какой будет epoch_shift, здесь нужна дополнительная логика,
        чтобы «восстановить», в какой именно эпохе мы находимся. Но если dt сам по себе
        строго в [1..9999], epoch_shift = 0.

        В более «продвинутом» варианте, когда dt сам может быть за пределами [1..9999],
        вы сделали бы итеративный цикл, чтобы «подогнать» dt в [DT_MIN..DT_MAX],
        а подсчитанное количество "полных шагов" EPOCH_RANGE сохранять в epoch_shift.

        Но штатный datetime в Python просто не даст создать объект вне [1..9999].
        """
        # Допустим, что dt уже корректен (1..9999).
        # Тогда просто вытаскиваем компоненты.
        raw_year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        microsecond = dt.microsecond

        # Здесь epoch_shift=0 (потому что dt уже в текущей эпохе).
        # Если бы нужно было восстанавливать сдвиг из dt,
        # надо было бы сравнить dt с каким-то базовым "якорем" и вычислять,
        # во сколько EPOCH_RANGE он уходит за пределы.
        # Но обычно Python не позволяет создать такой dt вовсе.
        epoch_shift = 0

        # Вычислим weekday
        wd = dt.weekday()

        return cls(
            year=raw_year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            relative_offset=timedelta(0),
            weekday=wd,
            epoch_shift=epoch_shift
        )

    def isoformat(self):
        """
        Для удобства выводим ISO-строку из "расширенного" datetime (to_extended_datetime).
        """
        return self.to_extended_datetime().isoformat()

    @classmethod
    def now(cls):
        dt = datetime.datetime.now()
        return cls(
            year=dt.year, month=dt.month, day=dt.day,
            hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=dt.microsecond
        )

    def replace(self, **kwargs):
        new_fields = {
            'year': kwargs.get('year', self.year),
            'month': kwargs.get('month', self.month),
            'day': kwargs.get('day', self.day),
            'hour': kwargs.get('hour', self.hour),
            'minute': kwargs.get('minute', self.minute),
            'second': kwargs.get('second', self.second),
            'microsecond': kwargs.get('microsecond', self.microsecond),
            'epoch_shift': kwargs.get('epoch_shift', self.epoch_shift),
        }
        new_offset = kwargs.get('relative_offset', self.relative_offset)
        new_weekday = kwargs.get('weekday', self._weekday)

        return PartialDateTime(
            **new_fields,
            relative_offset=new_offset,
            weekday=new_weekday
        )

    def __add__(self, other):
        if isinstance(other, timedelta):
            # Если у нас заданы все год/месяц/день, то корректнее сразу обратиться
            # к to_extended_datetime(), сложить timedelta, а потом распарсить обратно.
            if self.is_complete():
                extended = self.to_extended_datetime() + other
                # extended гарантированно в [1..9999] после сложения? Вдруг вышел за границы?
                # Тогда придётся снова "поднять" epoch_shift. Для простоты перегоним вручную:
                return self.from_extended_datetime(extended)
            else:
                # Если дата неполная, складываем только offset.
                new_offset = self.relative_offset + other
                # Корректируем weekday, если есть.
                if self._weekday is not None:
                    offset_days = int(other.total_seconds() // 86400)
                    new_weekday = (self._weekday + offset_days) % 7
                else:
                    new_weekday = None
                return PartialDateTime(
                    self.year, self.month, self.day,
                    self.hour, self.minute, self.second, self.microsecond,
                    relative_offset=new_offset,
                    weekday=new_weekday,
                    epoch_shift=self.epoch_shift
                )
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, timedelta):
            if self.is_complete():
                extended = self.to_extended_datetime() - other
                return self.from_extended_datetime(extended)
            else:
                new_offset = self.relative_offset - other
                if self._weekday is not None:
                    offset_days = int(other.total_seconds() // 86400)
                    new_weekday = (self._weekday - offset_days) % 7
                else:
                    new_weekday = None
                return PartialDateTime(
                    self.year, self.month, self.day,
                    self.hour, self.minute, self.second, self.microsecond,
                    relative_offset=new_offset,
                    weekday=new_weekday,
                    epoch_shift=self.epoch_shift
                )
        elif isinstance(other, PartialDateTime):
            # Чтобы корректно учесть эпохи, смотрим разницу между
            # двумя to_extended_datetime().
            dt1 = self.to_extended_datetime()
            dt2 = other.to_extended_datetime()
            return dt1 - dt2
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, PartialDateTime):
            try:
                return self.to_extended_datetime() == other.to_extended_datetime()
            except ValueError:
                # если одна из дат неполная и не может быть переведена
                return False
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, PartialDateTime):
            return self.to_extended_datetime() < other.to_extended_datetime()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, PartialDateTime):
            return self.to_extended_datetime() <= other.to_extended_datetime()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PartialDateTime):
            return self.to_extended_datetime() > other.to_extended_datetime()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PartialDateTime):
            return self.to_extended_datetime() >= other.to_extended_datetime()
        return NotImplemented

    def __str__(self):
        # Чисто для наглядности
        y = str(self.year) if self.year is not None else "????"
        m = f"{self.month:02d}" if self.month is not None else "??"
        d = f"{self.day:02d}" if self.day is not None else "??"
        hh = f"{self.hour:02d}" if self.hour is not None else "??"
        mm = f"{self.minute:02d}" if self.minute is not None else "??"
        ss = f"{self.second:02d}" if self.second is not None else "??"
        us = f"{self.microsecond:06d}" if self.microsecond is not None else "??????"

        base_str = f"{y}-{m}-{d} {hh}:{mm}:{ss}.{us}"
        if self.relative_offset != timedelta(0):
            base_str += f" +{self.relative_offset}"
        if self._weekday is not None:
            base_str += f" (weekday={self._weekday})"
        if self.epoch_shift != 0:
            base_str += f" [epoch_shift={self.epoch_shift}]"
        return base_str

    def __repr__(self):
        return (f"PartialDateTime(year={self.year}, month={self.month}, day={self.day}, "
                f"hour={self.hour}, minute={self.minute}, second={self.second}, "
                f"microsecond={self.microsecond}, relative_offset={self.relative_offset}, "
                f"weekday={self.weekday}, epoch_shift={self.epoch_shift})")

