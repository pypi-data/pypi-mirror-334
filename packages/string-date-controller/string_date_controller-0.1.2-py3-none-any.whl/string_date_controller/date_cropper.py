from .date_formatter import transform_date_nodashed_to_dashed

def get_final_date_of_timeseries(df):
    return df.index.dropna()[-1]

def get_initial_date_of_timeseries(df):
    return df.index.dropna()[0]

def get_initial_and_final_date_of_timeseries(df):
    dates = df.index.dropna()
    return (dates[0], dates[-1])

def extract_date_ref_from_file_name(file_name, option_dashed=True):
    date_ref = file_name.split('-at')[-1].split('-')[0]
    if option_dashed:
        date_ref = transform_date_nodashed_to_dashed(date_ref)
    return date_ref
