from helpers import *
from serialize import *

clean_serialization_folder()

#process the files
[lat1, long1, lat2, long2, lat_final, long_final, hours, duration, mean_speed, last_speed, last_last_speed] = pre_process_train_data()
serialize(lat1, "lat1")
serialize(long1, "long1")
serialize(lat2, "lat2")
serialize(long2, "long2")
serialize(lat_final, "lat_final")
serialize(long_final, "long_final")
serialize(hours, "hours")
serialize(duration, "duration")
serialize(mean_speed, "speed")
serialize(last_speed, "last_speed")
serialize(last_last_speed, "last_last_speed")

[lat1_t, long1_t, lat2_t, long2_t, hours_t, duration_t, mean_speed_t, last_speed_t, last_last_speed_t] = pre_process_test_data()
serialize(lat1_t, "lat1_t")
serialize(long1_t, "long1_t")
serialize(lat2_t, "lat2_t")
serialize(long2_t, "long2_t")
serialize(hours_t, "hours_t")
serialize(duration_t, "duration_t")
serialize(mean_speed_t, "speed_t")
serialize(last_speed_t, "last_speed_t")
serialize(last_last_speed_t, "last_last_speed_t")

print "Processing done. Program will exit."
