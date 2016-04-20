# INFOW18_FinalProject
This repository contains shared work for our final project exploring felony violence and school violence in NYC from 2006-2015.

[Project Proposal Google Doc](https://docs.google.com/document/d/1NgYAWtXdJbUWn-bTRg8dUD_qQlX3vMj29wX9dXT1TGc/edit)

[Project Report Google Doc](https://docs.google.com/document/d/1NgYAWtXdJbUWn-bTRg8dUD_qQlX3vMj29wX9dXT1TGc/edit)

[Project Data Google Folder](https://drive.google.com/open?id=0B0WZLk0rydoVMXdSVklScHpwbnc)

[Project GitHub Repo](https://github.com/mmillervedam/INFOW18_FinalProject)


---
## Links to Data Sources

Felony Data: https://catalog.data.gov/dataset/nypd-7-major-felony-incidents

School Safety Reports (VARDIS): http://www.p12.nysed.gov/irs/school_safety/school_safety_data_reporting.html

Population: https://catalog.data.gov/dataset/new-york-city-population-by-boroughs-fd2c0

---

## Links that may later be of use to us:

__ RE: NYC __

* [NYC Zoning Districts](http://www1.nyc.gov/site/planning/zoning/index-map.page) -- there are 31 of them but they don't seem to correspond to the numbers in our dataset.

* [NYC Maps and Demographic info](http://www.baruch.cuny.edu/nycdata/population-geography/index.html) -- courtesy of CUNY, includes links to maps of 'Districts' and 'Neighborhoods' , but again the number systems doesn't seem to match ours.

__ RE: School Data __

* [School Survey on Crime and Safety](http://nces.ed.gov/surveys/ssocs/data_products.asp) -- put out by the National Center for Ed Stats... probably less usefule b/c it uses random sampling and is not specific to NYC...

* [Dept of Ed Districts](http://schools.nyc.gov/schoolsearch/) -- school search website, the districts in our data set seem to be school districts but this site doesn't clearly lay out their lines.

* [School Locations](https://data.cityofnewyork.us/Education/School-Point-Locations/jfju-ynrr)

__ RE: Lat/Long calculations __
* [Stack Overflow post](http://stackoverflow.com/questions/1801732/how-do-i-link-to-google-maps-with-a-particular-longitude-and-latitude) talking about displaying longitude and latitiude coordinates on google maps:

* [Java script re: longitude and latitude](https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap)

* [Geographic Distance Tutorial](http://www.meridianworlddata.com/distance-calculation/)

* [Vincenty Package](https://pypi.python.org/pypi/vincenty)

* [Wikipedia Geographic Distance](https://en.wikipedia.org/wiki/Geographical_distance)
---

## PROJECT NOTES

* Juveniles are able to be charged with felonies. Generally, they are held as minors in Juvenile court (punishable until they are 18), but if it is not the first charge or if the prosecutor can present evidence that the child should be tried as an adult, then the child as young as 14 could be tried as an adult (judge’s decision). The judge has to do what is in the best interest of both the child and the public. In short, there could be overlap in our data of school violence and felonies in the area. Maybe we could definitely find the ones where  the address of the felony is at a school?
