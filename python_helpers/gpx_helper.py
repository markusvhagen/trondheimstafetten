import gpxpy
import gpxpy.gpx
import geopy.distance

def gradient_compute(elev_array,dist_array):
    gradient_array  = []
    step_rolling_average = 1
    for elev_element in elev_array:
        dist_element = dist_array[elev_array.index(elev_element)]
        if elev_element == elev_array[-step_rolling_average]:
            break
        rise = elev_array[elev_array.index(elev_element)+step_rolling_average] - elev_element
        run = dist_array[dist_array.index(dist_element)+step_rolling_average] - dist_element
        if run == 0:
            gradient = 0
        else:
            gradient = (rise/run)*100
        gradient_array.append(gradient)
    return gradient_array

gpx_file = open("gpx_files/Trondheim_stafetten_etappe_7.gpx", "r")

gpx = gpxpy.parse(gpx_file)

gps_array = []
z_array = []
non_filtered_z_array = []
total_dist = 0
dist_array = [0]

has_entered_point_loop = False

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            xyz = [point.latitude, point.longitude, point.elevation]
            xy = [point.latitude, point.longitude]
            z = [point.elevation]

            # compute distance between two points
            if has_entered_point_loop:
                new_coord = (xy[0],xy[1])
                increment = geopy.distance.geodesic(new_coord, prev_xy_coord).m
                total_dist = total_dist + increment
                dist_array.append(int(total_dist))

            gps_array.append([xy[1],xy[0]]) #have to switch the order because this is how mapbox reads coordinates
            z_array.append(int(z[0]))
            non_filtered_z_array.append(z[0])
            prev_xy_coord = xy
            if has_entered_point_loop == False:
                has_entered_point_loop = True
print("GPS:")
print(gps_array)
print("Elevation:")
print(z_array)
print("Distance:")
print(dist_array)
print("Gradient:")
print(gradient_compute(non_filtered_z_array,dist_array))


flat = 0
down = 0
up = 0
threshold = 1
for gradient in gradient_compute(non_filtered_z_array,dist_array):
    if abs(gradient) < threshold:
        flat += 1
    elif gradient < -threshold:
        down += 1
    else:
        up += 1

print("Flat: " + str(100*flat/(flat+down+up)) + "%, " + "Down: " + str(100*down/(flat+down+up)) + "%, " + "Up: " + str(100*up/(flat+down+up)) + "%.")
