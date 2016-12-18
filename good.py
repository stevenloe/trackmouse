import gps
import time

# Number of GPS fixes we've received:
numberOfFixes = 0
numberOfFixesInFinishZoneOnThisLap = 0
# Wall time when program starts. Wall time when Each lap starts.
time0 = time.time()

# Finish Line polygon:
polygon = [(39.733452,-105.026622),(39.733449,-105.026069),(39.732993,-105.026120),(39.732991,-105.026692)]


# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


while True:
	try:
		report = session.next()
		# Wait for a 'TPV' report and display the current time.
		# To see all report data, uncomment the line below"
		# print "##### START REPORT #####"
		#print report
		#print "###### END OF REPORT #######"
		#print " "
		if report['class'] == 'TPV':
			if hasattr(report, 'time'):
				print report.time
			if hasattr(report, 'lat'):
				print "Lat:" , report.lat, " Lon:", report.lon, " Speed:", report.speed, " Speed KPH:", report.speed * gps.MPS_TO_KPH, " Speed MPH:", report.speed * gps.MPS_TO_MPH
                haveWeCrossedFinish(report.lat, report.lon)
    except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "GPSD has terminated"




# point_in_poly came from: http://geospatialpython.com/2011/01/point-in-polygon.html
# Points were found with: https://itouchmap.com/latlong.html

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


# Create a timer loop and change the latitude. In each loop,
# test to see if we have crossed the finish line
# This code will cross the finish line in 14 iterations!!!


# This function does the following
#   1. Determines if the current fix is in the finish line polygon
#   2. Determines if we've just crossed the finish line
#   3. If we are not in the finish line polygon *and* we have more than 1 fix in the finishZone
#       We know that a lap has been started and we should start looking for another finish line
#       crossing. We do this by setting numberOfFixesInFinishZoneOnThisLap = 0
def haveWeCrossedFinish(lat, lon):
    print("haveWeCrossedFinish??")

    numberOfFixes += 1
    print("fix")

    hasCrossedFinishLine = point_in_poly(lat, lon, polygon)
    if hasCrossedFinishLine:
        numberOfFixesInFinishZoneOnThisLap += 1
        print(numberOfFixes, "lat", str(lat), "lon", str(lon), "hasCrossed", hasCrossedFinishLine)
        if numberOfFixesInFinishZoneOnThisLap == 1:
            # Get wall time
            if time0 > 0:
                elapsedTime = time.time() - time0, " Time seconds wall time "
            # store wall time at lap beginning so we can use it to calculate elapsedTime for the next lap:
            time0 = time.time()

            print("FINISH!!!! ", numberOfFixes, "lat", str(lat), "lon", str(lon), "elapsed:", elapsedTime)
    else:
        if numberOfFixesInFinishZoneOnThisLap > 1:
            # have we left the finish zone?
            print("Set the numberOfFixeser to 0. We should reset the location too")
            numberOfFixesInFinishZoneOnThisLap = 0






# NOTES
# in front of Grove Street ( From South Property line, to south end of block)
#polygon = [(39.733452,-105.026622),(39.733449,-105.026069),(39.732993,-105.026120),(39.732991,-105.026692)]

# Start point: 39.73379,-105.026376

# in front of grove street ( south of the house as that's where the boundary begins:
#point_x = 39.733350
#point_y = -105.026375

# North of boundary on grove street
#point_x = 39.733771
#point_y = -105.026383

## Call the function with the points and the polygon
# print(point_in_poly(point_x,point_y,polygon))
