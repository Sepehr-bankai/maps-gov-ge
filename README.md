<h1>GEORGIA MAP GOV<h1>

THE MAIN GOAL OF THIS PROJECT was that i find a way to get Cadastrial codes and Names of the owners of the Georgia's houses with greater speed and better way than clicking on the map.
the best way was to send API rquests simontenisly and a way to get that was to send the longtitute and latitude of the location in the form of JSON.
YOU CAAN SEE HOW IT WORKS BELOW...

# STEP ONE

<p1>at first, the **math-beta.py** will take a langtitute and longtitude as input,

then will ask for Raius as the outer border,
then will make a circle with the Radius that was given and make a JSON file dict structured of coordinates,

# STEP TWO

then when you execute **main.py** it will take the JSON output from the math-beta
as the input,

and sends Requests to the MAP.GOV.GE as API POST requests, with a default rate limit of 100 requests per minute.

EACH COORDINATE will be saved as a seperated Json file with dict structures.

