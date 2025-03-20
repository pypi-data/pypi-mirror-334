import icecream

import hors

# Распознавание фиксированной даты и времени
r = hors.process_phrase('С пира прошло 14 минут.')
icecream.ic(r.to_dict())

r = hors.process_phrase('С пира прошло полчаса.')
icecream.ic(r.to_dict())

r = hors.process_phrase('С пира прошло 1 час 14 минут')
icecream.ic(r.to_dict())

r = hors.process_phrase('С пира прошло 2 часа')
icecream.ic(r.to_dict())

r = hors.process_phrase('С пира прошло половина 1 часа')
icecream.ic(r.to_dict())
# print(r.dates[0].type)  # <DateTimeTokenType.FIXED: 1>
# print(f"{r.dates[0].date_from} | {r.dates[0].date_to}")
# ????-??-03 00:00:00.000000 | ????-??-03 00:00:00.000000 + 23:59:59.999999
