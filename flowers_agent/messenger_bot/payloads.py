import datetime
from collections import OrderedDict

GET_STARTED = 'GET_STARTED'

FLOWER_ADD = 'FLOWER_ADD'
FLOWER_SET_IMAGE = 'FLOWER_SET_IMAGE'

PERIOD_1D = '1D'
PERIOD_2D = '2D'
PERIOD_3D = '3D'
PERIOD_4D = '4D'
PERIOD_5D = '5D'
PERIOD_6D = '6D'
PERIOD_7D = '7D'
PERIOD_14D = '14D'

PERIOD_MAP = {
    PERIOD_1D: datetime.timedelta(days=1),
    PERIOD_2D: datetime.timedelta(days=2),
    PERIOD_3D: datetime.timedelta(days=3),
    PERIOD_4D: datetime.timedelta(days=4),
    PERIOD_5D: datetime.timedelta(days=5),
    PERIOD_6D: datetime.timedelta(days=6),
    PERIOD_7D: datetime.timedelta(days=7),
    PERIOD_14D: datetime.timedelta(days=14),
}

WATERING_PERIODS = OrderedDict([
    (PERIOD_1D, '1 dzień'),
    (PERIOD_2D, '2 dni'),
    (PERIOD_3D, '3 dni'),
    # TODO: buttons template supports maximum 3 buttons
    # (PERIOD_4D, '4 dni'),
    # (PERIOD_5D, '5 dni'),
    # (PERIOD_6D, '6 dni'),
    # (PERIOD_7D, 'tydzień'),
    # (PERIOD_1D, '2 tygodnie'),
])

# TODO: implement support for payload below
SHOW_ALL_FLOWERS = 'SHOW_ALL_FLOWERS'
SHOW_TODAYS_FLOWERS = 'SHOW_TODAYS_FLOWERS'
