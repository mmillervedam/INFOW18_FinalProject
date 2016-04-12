# INFOW18_FinalProject
Repo for our shared work on the final project.

[Project Proposal Google Doc](https://docs.google.com/document/d/1NgYAWtXdJbUWn-bTRg8dUD_qQlX3vMj29wX9dXT1TGc/edit)

===

The Proposal

With your group come up with a 2 page proposal about the questions that you intend to ask of the data. This should include:

Initial plots, figures or tables.
References to column names and the analysis that they may provide.
Additional datasets that you plan on including in your analysis like the weather data. This means links, columns that you'll join on, etc.
What you plan to cover in the final report and how you plan on organizing it.
Who is in your group.
You should have started digging into your analysis at this point and the proposal is an expression of its viability to the instructors. We should have the sense that this is something you will be able to deliver on (and that the data will support you in doing so).

THE PROPOSAL IS DUE BY APRIL 12.

Data Repository: Use "git clone [link]" to create a new local repository we can all share. Repository is found here. Note that the data is NOT in the repository (too large). https://github.com/mmillervedam/INFOW18_FinalProject

Data: The goal is to combine these datasets by "borough" to get more interesting revelations from our analysis for the final project.

Felony Data: https://catalog.data.gov/dataset/nypd-7-major-felony-incidents

School Safety: https://catalog.data.gov/dataset/school-safety-report-8067a

Population: https://catalog.data.gov/dataset/new-york-city-population-by-boroughs-fd2c0

===

## Links that may later be of use to us:

* [Stack Overflow post](http://stackoverflow.com/questions/1801732/how-do-i-link-to-google-maps-with-a-particular-longitude-and-latitude) talking about displaying longitude and latitiude coordinates on google maps:

* [VARDIS](http://www.p12.nysed.gov/irs/school_safety/school_safety_data_reporting.html) - NYC school incident data for 2008-2014

* [School Survey on Crime and Safety](http://nces.ed.gov/surveys/ssocs/data_products.asp) -- put out by the National Center for Ed Stats... probably less usefule b/c it uses random sampling and is not specific to NYC...

* [Dept of Ed Districts](http://schools.nyc.gov/schoolsearch/) -- school search website, the districts in our data set seem to be school districts but this site doesn't clearly lay out their lines.

* [NYC Zoning Districts](http://www1.nyc.gov/site/planning/zoning/index-map.page) -- there are 31 of them but they don't seem to correspond to the numbers in our dataset.

* [NYC Maps and Demographic info](http://www.baruch.cuny.edu/nycdata/population-geography/index.html) -- courtesy of CUNY, includes links to maps of 'Districts' and 'Neighborhoods' , but again the number systems doesn't seem to match ours.

* [Java script re: longitude and latitude](https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap)

* [School Locations](https://data.cityofnewyork.us/Education/School-Point-Locations/jfju-ynrr)
=======
## NOTES

* Juveniles are able to be charged with felonies. Generally, they are held as minors in Juvenile court (punishable until they are 18), but if it is not the first charge or if the prosecutor can present evidence that the child should be tried as an adult, then the child as young as 14 could be tried as an adult (judge’s decision). The judge has to do what is in the best interest of both the child and the public. In short, there could be overlap in our data of school violence and felonies in the area. Maybe we could definitely find the ones where  the address of the felony is at a school?
