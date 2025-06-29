#  Real-Time Flight Tracker (Python + OpenSky API)

This is a small Python script that pulls live flight data from the OpenSky Network API and shows it in your terminal.  
It refreshes every 10 seconds and displays basic info like callsign, country, altitude, speed, and location.

Just a fun little project to mess around with real-time flight tracking.

---

##  What It Does

- Grabs real-time flight data from OpenSky API  
- Prints the first 10 aircraft in a clean table  
- Refreshes every 10 seconds  
- No hardware or setup needed – just Python and an internet connection

---

##  Requirements

- Python 3.x
- requests and tabulate libraries

Install them using pip if needed:

pip install requests tabulate
