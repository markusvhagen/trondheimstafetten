import gpxpy
import gpxpy.gpx
import geopy.distance

gpx_file = open("gpx_files/Trondheim_stafetten_etappe_4.gpx", "r")

gpx = gpxpy.parse(gpx_file)

gps_array = []
z_array = []
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
            prev_xy_coord = xy
            if has_entered_point_loop == False:
                has_entered_point_loop = True
print("GPS:")
print(gps_array)
print("Elevation:")
print(z_array)
print("Distance:")
print(dist_array)
