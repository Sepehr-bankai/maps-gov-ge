<h1>GEORGIA MAP GOV<h1>


**step 1**
at first, the **math-beta.py** will take a langtitute and longtitude as input,
then will ask for Raius as the outer border,
then will make a circle with the Radius that was given and make a JSON file dict structured of coordinates,

**step2**
then when you execute **main.py** it will take the JSON output from the math-beta
as the input,
and sends Requests to the MAP.GOV.GE as api POST, with the rate limit of 1 request per second.
EACH COORDINATE will be saved as a seperated Json file with dict structures.

