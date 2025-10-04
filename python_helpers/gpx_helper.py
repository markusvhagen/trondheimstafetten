import gpxpy
import gpxpy.gpx

gpx_file = open("gpx_files/activity_20514376271.gpx", "r")

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            xyz = [point.latitude, point.longitude, point.elevation]
            xy = [point.latitude, point.longitude]
            print("[" + str(xy[1]) + ", " + str(xy[0]) + "]" + ",") #have to switch the order because this is how mapbox reads coordinates
