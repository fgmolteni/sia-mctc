from datetime import datetime as dt, date, time
import numpy as np

from components.constants import LimitesViaje




def calculate_days(start_date_str, end_date_str, date_format="%Y-%m-%d %H:%M"):
    """
    Calculates the number of days between two date-time strings.

    Args:
        start_date_str (str): The start date and time in the specified format.
        end_date_str (str): The end date and time in the specified format.
        date_format (str): The format of the input date strings. 
        Default is "%Y-%m-%d %H:%M".

    Returns:
        numpy.float16: The total number of days between the two dates.
    """
    try:
        start_date = dt.strptime(start_date_str, date_format)
        end_date = dt.strptime(end_date_str, date_format)
        
        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        time_difference = end_date - start_date
        
        # Return the total number of days, including fractions
        return np.float16(time_difference.total_seconds() / (24 * 3600))

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def calculate_travel_expenses(date_start, date_end, time_start, time_end, distance_travel):
    # Calculate the number of full days between the start and end dates
    days_travel_expenses = (date_end - date_start).days

    # Define the reference time (12:00 PM)
    noon = time(12, 0)

    # Add days based on the time condition
    if ((time_start <= noon) and (time_end >= noon)) & (distance_travel > LimitesViaje.DISTANCIA_MINIMA_VIATICOS.value):
        days_travel_expenses += 1
    elif (time_end >= noon):
        days_travel_expenses +=1
        
    else:
        days_travel_expenses += 0.5
        
    return days_travel_expenses