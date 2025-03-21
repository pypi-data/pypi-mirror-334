import datetime
import pandas as pd
from typing_extensions import Literal

from .field_parser import FieldParser
from pancham.data_frame_field import DataFrameField

class DateTimeFieldParser(FieldParser):

    FUNCTION_ID = "datetime"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        format = '%d/%m/%Y'
        on_error: Literal['coerce', 'ignore', 'raise'] = 'raise'

        if type(field[self.FUNCTION_KEY][self.FUNCTION_ID]) is dict:
            format = field[self.FUNCTION_KEY][self.FUNCTION_ID].get('format', '%d/%m/%Y')

            on_error = field[self.FUNCTION_KEY][self.FUNCTION_ID].get('on_error', 'raise')
            if on_error not in ['coerce', 'ignore', 'raise']:
                on_error = 'raise'

        return DataFrameField(
            name = field['name'],
            field_type=datetime.datetime,
            nullable=self.is_nullable(field),
            source_name=None,
            func=lambda x: pd.to_datetime(x[self.get_source_name(field)], format=format, errors=on_error)
        )