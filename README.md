# HypeMan
HypeMan brings the hype.  This is the legacy of Rob's original Hypeman.  Rob has left coding for the time being but I will be maintaining Hypeman to work with DCS updates as they come and introducing small feature updates as I can.

# Introduction
`hypeMan_flightlog.lua` -  This is the script that gets included with your DCS mission.

`hypeman_listener.lua` - this is the backend listener that receives the messages from Discord and sends the messages to Discord

## Requirements:
- Mist 4.4 or higher
- Discordia lua Discord API
- luvit lua REPL or similar
- MOOSE develop branch dated after 12-29-21 for full Airboss and Rangeboss outputs

## INSTALLATION

Download the GitHub files into C:/HypeMan

Then include the hypeMan_flightlog.lua file in your mission with a DO SCRIPT, or DO SCRIPT FILE any time after Mist/MOOSE has been loaded.

TIPS AND TRICKS
Load HypeMan from an external file using this DO SCRIPT:
```
assert(loadfile("C:/HypeMan/HypeMan_flightlog.lua"))() 
```

This allows HypeMan to be updated for every mission it is included with by simply changing the external file.
Simply add that code to any mission, even if you do not have HypeMan running or installed.  Because the loadfile
is wrapped in an assert() call any errors are supressed.

The `MissionScripting.lua` located in X:\Eagle Dynamics\DCS World OpenBeta\Scripts will need to be modified to allow Hypeman to communicate out of DCS.

The following lines should be commented out,  `io` and `lfs` will generally be required for MOOSE to work and `require` and `package` will need to be commented out for Hypeman to work properly. These changes will get written over by dcsupdater after each patch from Eagle Dynamics and will need to be updated.  Before making any changes always back up your original files.

Example:
```
do
	sanitizeModule('os')
	--sanitizeModule('io')  --comment out
	--sanitizeModule('lfs')  --comment out
	--_G['require'] = nil   --comment out
	_G['loadlib'] = nil
	--_G['package'] = nil  --comment out
end
```

## USAGE

Once loaded, HypeMan monitors for several events: takeoffs, landings, crash, eject, etc, and will automatically report
these events to Discord.
HypeMan also provides a function that can be called anywhere in the mission: hypeman.sendBotMessage().  This allows
Mission creators to send messages to the Discord based on events in the mission.

-- i.e. TRIGGER TYPE ONCE, IF GROUP DEAD('RED TANKS') THEN DO SCRIPT `hypeman.sendBotMessage('The Red Tanks have been destroyed!  Move forward!')`

## Discord Bots

For this to work you will need to hook a discord bot into your Discord server and let it access writing to channels.  
Access the [Discord Developer Portal](https://discord.com/developers/applications) , create a 'New Application', set permissions and then access your bot token.  This will be placed into the `private_api_keys.lua` file along with the specific channel IDs. 

## FAQ

1.) I'm worried about performance and stability.  Does HypeMan take a lot of resources in the mission?

HypeMan is pretty light, and the messages are sent over UDP with no locking or waiting for acknowledgement.  HypeMan should not negatively impact server or mission performance.

2.) Because all multiplayer clients get a full copy of the .miz file in the multiplayer track, won't that expose my private Discord bot API key to every multiplayer client?

No, the private Discord API key is only used by the Hypeman_listener.lua backend, and this file is not included with the DCS .miz file, so no private API keys are exposed to multiplayer clients.

3.) I want to stop HypeMan from sending messages while I experiment with the Server

Simply stop the hypeman_listener backend.  The backend listener can be started, stopped, and restarted at any time while the mission is running.

4.) I don't want to install HypeMan on the many computers I edit DCS missions on, and I want virtual squadron members to be able to edit missions and not worry about having to have all these external .lua file dependencies.

```
assert(loadfile("C:/HypeMan/HypeMan_flightlog.lua"))() 
```

Using the assert/loadfile code snippet to load HypeMan means that if the lua file is not found, the errors are just supressed and the mission will continue even if HypeMan is not found.

## Python Installation for Trap/Targetsheets

Hypeman will generate text outputs to Discord through a bot.  However, if you are looking for the discord graphs, it requires an Anaconda install in order to produce them using mathplotlib.  Below is a basic manual on how to install Anaconda and get DCS to talk to Anaconda when Events happen.

See 'Conda Install.docx' or access it in [google docs.](https://docs.google.com/document/d/e/2PACX-1vTGR67SZMlLo8FRF8aMG17fOhOqAB1Z-zs9WTFE6A_dnZrabC_rQKbEwLOLrNF69YWZDKkq2VzT3vJB/pub)

Example trapsheet utilizing [MOOSE Airboss.](https://flightcontrol-master.github.io/MOOSE_DOCS_DEVELOP/Documentation/Ops.Airboss.html)
![Graphic](https://github.com/robscallsign/HypeMan/blob/master/Manual%20Images/trapsheet.png?raw=true)
Greenie Board
![Graphic](https://github.com/robscallsign/HypeMan/blob/master/Manual%20Images/final.jpg?raw=true)
Example targetsheet utilizing [MOOSE RangeBoss](https://flightcontrol-master.github.io/MOOSE_DOCS_DEVELOP/Documentation/Functional.Range.html)
![Graphic](https://github.com/robscallsign/HypeMan/blob/master/Manual%20Images/targetSheet.png?raw=true)

## Headers for google sheets

These are needed in your google sheets to prevent errors in the python code.
LSO
```pilot    grade    points    finalscore    details    wire    Tgroove    case    wind    modex    airframe    carriertype    carriername    theatre    mitime    midate    ServerName    ServerDate    ServerTime```

RangeBoss
```pilot    aircraftType    weaponType    impactDistance    impactRadial    impactQuality    bombScore    altitude    pitch    strafeAccuracy    strafeQuality    strafeScore    roundsFired    roundsHit    theatre    rangeName    missionType    mizTime    mizDate    osDate    osTime    serverName```

FlightLogs
```Callsign    FlightTime    AircraftType    TakeOffs    Landings    DepartureField    ArrivalField1    ArrivalField2    Coalition    MissionType    ServerName    ServerDate    ServerTime    Theatre    Dead    Crashed    Ejected    Refueled    Failure    AirStart    MissionEnd```
