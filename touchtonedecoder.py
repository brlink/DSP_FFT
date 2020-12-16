import numpy as np

"""
find the start point from last end point
"""


def point_start(last_end):
    for i in range(last_end, len(ecg)):
        # set reference point
        reference_point = i
        # set a counter
        valid_counter = 0
        # compare 100 points right after reference point, if there are more than 50
        # differences greater than 10, than this point is start point
        for j in range(1, 101):
            if reference_point == len(ecg) - 100:
                return None
            # set compare point
            compare_point = i + j
            compare_point_val = ecg[compare_point]
            # get difference
            difference = abs(base_amplitude - compare_point_val)
            if difference > 10:
                if valid_counter >= 50:
                    return np.math.ceil(reference_point / 1000) * 1000
                # add counter
                valid_counter += 1


"""
find the end point from last start point
"""


def point_end(last_start):
    for i in range(last_start, len(ecg)):
        # set reference point
        reference_point = i
        # set a counter
        valid_counter = 0
        # compare 100 points right after reference point, if there are more than 80
        # differences smaller than 10, than this point is end point
        for j in range(1, 101):
            if reference_point == len(ecg) - 100:
                return None
            # set compare point
            compare_point = i + j
            compare_point_val = ecg[compare_point]
            # get difference
            difference = abs(base_amplitude - compare_point_val)
            if difference < 10:
                if valid_counter >= 80:
                    return np.math.ceil(reference_point / 1000) * 1000
                # add counter
                valid_counter += 1


def single_chunk(last_end):
    # initial return value
    return_val = []
    # get new start point
    new_start = point_start(last_end)
    # get new end point
    new_end = point_end(new_start)
    # add end point
    return_val.append(new_end)
    # split the time zone
    temp_ecg = ecg[new_start:new_end]
    # fft
    temp_ecg_fft = np.fft.fft(temp_ecg)
    # define frequency zone
    freq_axis = np.linspace(0, 1000, len(temp_ecg))
    # turn to absolute number
    for i, data in enumerate(temp_ecg_fft):
        temp_ecg_fft[i] = abs(data)
    # array store possible points
    possible_point = []
    # if a point greater than another 2 points beside it, than it might be a peak point
    for i in range(1, len(temp_ecg_fft) - 1):
        if temp_ecg_fft[i] > temp_ecg_fft[i + 1] and temp_ecg_fft[i] > temp_ecg_fft[i - 1]:
            possible_point.append(temp_ecg_fft[i])
    # sort array
    possible_point = sorted(possible_point)
    # find the location of the greatest 2 peaks
    # since the periodicity and symmetry, there are two pairs of high and low peaks
    location = np.where(temp_ecg_fft == possible_point[-1])
    high_freq = freq_axis[location[0][0]]
    location = np.where(temp_ecg_fft == possible_point[-3])
    low_freq = freq_axis[location[0][0]]

    def format_freq(loc_point):
        loc_point = int(loc_point)
        if loc_point > 500:
            loc_point = 1000 - loc_point
        return loc_point

    # get high and low frequency
    high_freq = format_freq(high_freq) + 1000
    low_freq = 1000 - format_freq(low_freq)

    for i in range(0, 10):
        reference = REFERENCE_ARRAY[i]
        if abs(reference[0] - low_freq) < 40 and abs(reference[1] - high_freq) < 40:
            return_val.append(i)

    return return_val


"""
main program
"""


def main():
    # initial start point
    start_point = ORIGINAL_END
    # initial all key number store array
    all_key = []
    while True:
        if point_start(start_point) is not None:
            receive_val = single_chunk(start_point)
            start_point = receive_val[0]
            all_key.append(receive_val[1])
        else:
            break
    print(all_key)


if __name__ == '__main__':
    # load dat file
    dat_file = np.loadtxt("touchtones.dat")
    ecg = dat_file[:, 1]
    # base amplitude
    base_amplitude = ecg[-1]
    # initial the original end point
    ORIGINAL_END = 0
    # initial reference array
    REFERENCE_ARRAY = [
        [941, 1336],  # 0
        [697, 1209],  # 1
        [697, 1336],  # 2
        [697, 1477],  # 3
        [770, 1209],  # 4
        [770, 1336],  # 5
        [770, 1477],  # 6
        [852, 1209],  # 7
        [852, 1336],  # 8
        [852, 1477]   # 9
    ]
    main()
