### functional_programming

from datetime import datetime, timedelta
from typing import Union, List
from functools import partial

def parse_date_format(date_str: str) -> tuple[str, bool]:
   """Determine the format of date string"""
   return ('%Y-%m-%d', True) if '-' in date_str else ('%Y%m%d', False)

def validate_dates(start: datetime, end: datetime) -> None:
   """Validate date range"""
   if start > end:
       raise ValueError("Start date must be earlier than or equal to end date")

def convert_to_datetime(date_input: Union[str, int], date_format: str) -> datetime:
   """Convert input to datetime object"""
   return datetime.strptime(str(date_input), date_format)

def generate_date_range(start: datetime, end: datetime) -> List[datetime]:
   """Generate list of datetime objects between two dates"""
   return [start + timedelta(days=x) for x in range((end - start).days + 1)]

def format_date(date: datetime, use_hyphen: bool) -> str:
   """Convert datetime object to string in specified format"""
   return date.strftime('%Y-%m-%d' if use_hyphen else '%Y%m%d')

def get_all_dates_between_dates(start_date: Union[str, int], end_date: Union[str, int]) -> List[str]:
   """
   Return list of all dates between two dates
   
   Args:
       start_date: Start date (YYYY-MM-DD or YYYYMMDD format)
       end_date: End date (same format as start_date)
   
   Returns:
       List[str]: List of dates from start_date to end_date
   
   Raises:
       ValueError: Invalid date format or start_date later than end_date
   """
   try:
       # 1. Parse date format
       date_format, use_hyphen = parse_date_format(str(start_date))
       
       # 2. Convert to datetime objects
       to_datetime = partial(convert_to_datetime, date_format=date_format)
       start = to_datetime(start_date)
       end = to_datetime(end_date)
       
       # 3. Validate dates
       validate_dates(start, end)
       
       # 4. Generate and format date range
       to_string = partial(format_date, use_hyphen=use_hyphen)
       
       return list(map(to_string, generate_date_range(start, end)))
       
   except ValueError as e:
       raise ValueError(f"Invalid date format or invalid date range: {str(e)}")