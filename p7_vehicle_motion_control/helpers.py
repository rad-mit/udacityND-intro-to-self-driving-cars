import pickle

def process_data(filename):
    with open(filename, 'rb') as f:
        data_list = pickle.load(f)
    return list(data_list)

def get_column(table, column_num):
    return [r[column_num] for r in table]

def get_derivative_from_data(position_data, time_data):
    """
    Calculates a list of speeds from position_data and 
    time_data.
    
    Arguments:
      position_data - a list of values corresponding to 
        vehicle position
 
      time_data     - a list of values (equal in length to
        position_data) which give timestamps for each 
        position measurement
    
    Returns:
      speeds        - a list of values (which is shorter 
        by ONE than the input lists) of speeds.
    """
    # 1. Check to make sure the input lists have same length
    if len(position_data) != len(time_data):
        raise(ValueError, "Data sets must have same length")
    
    # 2. Prepare empty list of speeds
    speeds = []
    
    # 3. Get first values for position and time
    previous_position = position_data[0]
    previous_time     = time_data[0]
    
    # 4. Begin loop through all data EXCEPT first entry
    for i in range(1, len(position_data)):
        
        # 5. get position and time data for this timestamp
        position = position_data[i]
        time     = time_data[i]
        
        # 6. Calculate delta_x and delta_t
        delta_x = position - previous_position
        delta_t = time - previous_time
        
        # 7. Speed is slope. Calculate it and append to list
        speed = delta_x / delta_t
        speeds.append(speed)
        
        # 8. Update values for next iteration of the loop.
        previous_position = position
        previous_time     = time
    
    return speeds

def get_integral_from_data(acceleration_data, times):
    # 1. We will need to keep track of the total accumulated speed
    accumulated_speed = 0.0
    
    # 2. The next lines should look familiar from the derivative code
    last_time = times[0]
    speeds = []
    
    # 3. Once again, we lose some data because we have to start
    #    at i=1 instead of i=0.
    for i in range(1, len(times)):
        
        # 4. Get the numbers for this index i
        acceleration = acceleration_data[i]
        time = times[i]
        
        # 5. Calculate delta t
        delta_t = time - last_time
        
        # 6. This is an important step! This is where we approximate
        #    the area under the curve using a rectangle w/ width of
        #    delta_t.
        delta_v = acceleration * delta_t
        
        # 7. The actual speed now is whatever the speed was before
        #    plus the new change in speed.
        accumulated_speed += delta_v
        
        # 8. append to speeds and update last_time
        speeds.append(accumulated_speed)
        last_time = time
    return speeds
