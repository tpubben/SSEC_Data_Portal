**This application requires the following dependencies:**

  - Django

# Description

Web portal for our clients to log in and see any pipeline or site methane leak inspection results.

## Web Maps: 

Geospatial data stored in PostGIS database and accessed via Django model framework. GeoJson created on the fly for methane sensor points and geometries of client sites and pipelines. Displayed using customized leaflet web map.

## Reports:

Reports are displayed using custom templates that allow our clients to mark down when they have repaired any detected leaks as well as allows for photos to be taken of pinpointed leaks so field personnel can identify and repair them in a timely fashion.

New reports and new leaks can only be added by superusers as specified by the company implementing the portal.

# Screenshots

![Report List](Report_list.PNG?raw=true "Report List")

![Edit Report](Edit_report_screenshot.PNG?raw=true "Edit Report")

![Report View Unrepaired](Report_view_screenshot_not_repaired.PNG?raw=true "Report View Unrepaired Leak")

![Report View Repaired](Report_view_screenshot_repaired.PNG?raw=true "Report View Repaired Leak")

![Add Leak](Add_leak_screenshot.PNG?raw=true "Add Leak")
