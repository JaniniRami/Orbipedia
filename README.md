# Orbipedia
A space tracker made to track all satellites infromation, live locations and orbits.

# Introduction
Now, more than ever, private and public space exploration companies such Space-X, NASA, and Blue Origin are sending out rockets. Equipped with all kinds of exploration and science payloads, the increase in launches has made it ever hard for the space enthusiasts to keep up to date. To address this, today, I would like to introduce you to [Orbipedia](https://github.com/JaniniRami/Orbipedia): A space track website that allows you to search space payloads and show their live location. 
<br>
![Orbipedia Home](https://github.com/JaniniRami/Orbipedia/blob/main/imgs/1.png?raw=true)
<br>
![Orbipedia Map](https://github.com/JaniniRami/Orbipedia/blob/main/imgs/2.png?raw=true)
# Setup Instructions
- Head to [space-track](https://www.space-track.org) and create an account.
- Clone Orbipedia: ```git clone https://github.com/JaniniRami/Orbipedia```.
- Enter your space track credentials in <b>credentials.py</b> file.
- Install the requirements for Orbipedia: ```python3 -m pip install -r requirements.txt```.
- Run Orbipedia website: ```python3 app.py```.
- Head to <b>localhost:5000</b> in your browser and enjoy!

# How it works
Orbipedia uses python flask library to retrieve data from the [space-track](https://www.space-track.org) API, clean and process the data, and sends it to the front end website. After doing so, the front end processes the TLE lines of the selected space object and uses [satellite.js](https://github.com/shashwatak/satellite-js) library to decode the TLE lines and show the live location of the selected space object and the orbit of it. In order to visually display the object’s live location, [Open Layers](https://openlayers.org/) maps are used.

# Contributions
Contributions to fix bugs or to add new features are open, just make your pull request and I will be here to review it and merge it as soon as possible!

# Resources
- Satellite data source: [space-track](https://www.space-track.org)
- Library used to process all the TLE lines: [satellite.js](https://github.com/shashwatak/satellite-js)
- Library used to draw the map: [Open Layers](https://openlayers.org/)

