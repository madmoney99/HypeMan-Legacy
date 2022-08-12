----------------RANGEBOSS EXAMPLE--------------------
local bombtargets={"North Circle", "South Circle"}
local strafepit={"Strafe Pit"}
local foulline={"Foul Line"}
X_Airstrip=RANGE:New("X-Airstrip Range")
X_Airstrip:AddBombingTargets(bombtargets)
X_Airstrip:AddBombingTargetGroup(GROUP:FindByName("Russian BMPs"), 50, false)
X_Airstrip:SetRangeRadius(10)
rangeFoul=X_Airstrip:GetFoullineDistance("Strafe Pit", "Foul Line")
X_Airstrip:AddStrafePit(strafepit,3000,300,nil,false,20,rangeFoul)

function X_Airstrip:OnAfterEnterRange(From, Event, To, player)
 local text=string.format("%s has entered the %s", player.playername, self.rangename)  
 HypeMan.sendBotMessage(text)
end

function X_Airstrip:OnAfterExitRange(From, Event, To, player)
 local text=string.format("%s has exited the %s Range", player.playername, self.rangename)  
 HypeMan.sendBotMessage(text)
end

function X_Airstrip:OnAfterImpact(From, Event, To, result, player)  
   result.messageType = 4
   result.callsign = player.playername
   result.theatre = env.mission.theatre
   result.rangeName = self.rangename
   result.missionType = "1"
   result.mizTime = UTILS.SecondsToClock(timer.getAbsTime())
   result.midate=UTILS.GetDCSMissionDate()
   result.strafeAccuracy = "N/A"
   result.strafeQuality = "N/A"
   result.altitude = playerAltForRangeData*3.28084
   result.pitch = playerPitchForRangeData
   result.heading = playerHeadingForRangeData
   _playername = player.playername 
   result.strafeScore = "N/A"
   result.bombScore = "notSet"

   if result.quality == "SHACK" then
       result.bombScore = "5"
   elseif result.quality == "EXCELLENT" then
       result.bombScore = "4"
   elseif result.quality == "GOOD" then
       result.bombScore = "3"
   elseif result.quality == "INEFFECTIVE" then
       result.bombScore = "2"
   elseif result.quality == "POOR" then
       result.bombScore = "1"	
   end

   HypeMan.sendBotTable(result)
   self:_SaveTargetSheet(_playername, result) 
   
   if result.distance <= 1.52 then
       --trigger.action.outSound("Airboss Soundfiles/sureshot.ogg")
   end
end

local strafezone = ZONE:New("StrafeZone")

function displayStrafeResults()
       local name = Straferesult.player
       local quality = Straferesult.roundsQuality
       
   if  clientStrafed == true then
       result={}
       result.messageType = 4 
       result.callsign = Straferesult.player
       result.airframe = Straferesult.airframe 
       result.theatre = env.mission.theatre
       result.rangeName = Straferesult.rangename
       result.missionType = "1"
       result.mizTime = UTILS.SecondsToClock(timer.getAbsTime())
       result.strafeAccuracy = Straferesult.strafeAccuracy 
       result.midate=UTILS.GetDCSMissionDate()
       result.strafeScore = "notSet"
       result.bombScore = "N/A"
       if invalidStrafe == true then
           result.roundsQuality = "* INVALID - PASSED FOUL LINE *"
           result.strafeScore = "0"
       else
           result.roundsQuality = Straferesult.roundsQuality
           
           if result.roundsQuality == "DEADEYE PASS" then
               result.strafeScore = "5"
               result.roundsQuality = "DEADEYE"
           elseif result.roundsQuality == "EXCELLENT PASS" then
               result.strafeScore = "4"
               result.roundsQuality = "EXCELLENT"
           elseif result.roundsQuality == "GOOD PASS" then
               result.strafeScore = "3"
               result.roundsQuality = "GOOD"
           elseif result.roundsQuality == "INEFFECTIVE PASS" then
               result.strafeScore = "2"
               result.roundsQuality = "INEFFECTIVE"
           elseif result.roundsQuality == "POOR PASS" then
               result.strafeScore = "1"
               result.roundsQuality = "POOR"
           elseif result.roundsQuality == "* INVALID - PASSED FOUL LINE *" then
               result.strafeScore = "0"
           else
               result.strafeScore = "ERROR"
           end
       end

       result.quality = Straferesult.quality 
       result.roundsFired = Straferesult.roundsFired
       result.roundsHit = Straferesult.roundsHit 

       if result.airframe == "FA-18C_hornet" or "F-14A-135-GR" or "F-14B" or "F-16C_50" or "F-15C" or "VSN_F104G" then
            result.weapon = "M61A1 Vulcan"
        elseif result.airframe == "AV8BNA" then
            result.weapon = "GAU-12 Equalizer"
        elseif result.airframe == "M-2000C" then
            result.weapon = "DEFA 554"
        elseif result.airframe == "F-5E-3" then
            result.weapon = "20 mm M39A2 Revolver cannon"
        elseif result.airframe == "A-10C" or "A-10C_2" then
            result.weapon = "GAU-8/A Avenger"
        elseif result.airframe == "UH-1H" then
            result.weapon = "M134 minigun" 
        elseif result.airframe == "P-51D-30-NA" then
            result.weapon = "0.50 caliber AN/M2 Browning machine guns"
        elseif result.airframe == "F-86" then
            result.weapon = "0.50 caliber AN/M3 Browning machine guns"
        elseif result.airframe == "A-4E-C" then
			result.weapon = "Colt Mk 12 cannon"			
        else
            result.weapon = "(unknown)CANNON"
        end
       
       result.radial = 0
       result.distance = 0
       result.altitude = playerAltForRangeData*3.28084
       result.pitch = playerPitchForRangeData
       result.heading = playerHeadingForRangeData
       HypeMan.sendBotTable(result)
       env.info('Range_Discord_reporting_script RANGE Script: SENT:  HypeMan.sendBotTable(result)')

       if result.strafeAccuracy >= 90 then
           env.info('Range_Discord_reporting_script RANGE Script: STRAFE:  accuracy greater than or equal to 90% ')
           dead_eye()
           --trigger.action.outSound("Airboss Soundfiles/sureshot.ogg")
       else
           env.info('Range_Discord_reporting_script RANGE Script: STRAFE:  accuracy less than 75% ')
       end
       result = nil
   else
       trigger.action.outText('STRAFE:  NOT SHOWING RESULTS, A FALSE/UNINTENDED STRAFE RUN ', 5 )

   end
   clientRollingIn = false
   clientStrafed = false
   invalidStrafe = false
end

local SetClient = SET_CLIENT:New():FilterCoalitions("blue"):FilterStart()

function CLIENT_IN_STRAFE_PIT_ZONE()
   SetClient:ForEachClient(function(client)
       if (client ~= nil) and (client:IsAlive()) then 
         local clientheading  = client:GetHeading()
         local pitheading   = 090 --********  Change this to the strafe attack heading!!!!! 
         local deltaheading = clientheading-pitheading
         local towardspit   = math.abs(deltaheading)<=90 or math.abs(deltaheading-360)<=90
         local playerName = client:GetPlayerName()
         
         if clientRollingIn == true then 
           local text = (playerName..' rolling into Strafe Pit ')
           HypeMan.sendBotMessage(text)
           clientRollingIn = false
           timer.scheduleFunction(displayStrafeResults, {}, timer.getTime() + 13)
         else
         end

       end
end)
timer.scheduleFunction(CLIENT_IN_STRAFE_PIT_ZONE,nil,timer.getTime() + 3)
end
CLIENT_IN_STRAFE_PIT_ZONE()

GunFireStart = EVENTHANDLER:New():HandleEvent(EVENTS.ShootingStart)
ShootingEvent = EVENTHANDLER:New():HandleEvent(EVENTS.Shot)

function GunFireStart:OnEventShootingStart(EventData)
    if EventData.IniPlayerName ~= nil then 
        local PlayerName = EventData.IniPlayerName
            local PlayerUnit = EventData.IniUnit
            playerAltForRangeData = PlayerUnit:GetAltitude()
            playerPitchForRangeData = PlayerUnit:GetPitch()
            playerHeadingForRangeData = PlayerUnit:GetHeading()
            weaponUsedScript = "cannon rounds"    
    end
end

function ShootingEvent:OnEventShot(EventData)    
    if EventData.IniUnit:GetCoalitionName() == "Blue" then
        if EventData.IniPlayerName ~= nil then 
            local PlayerUnit = EventData.IniUnit
            playerAltForRangeData = PlayerUnit:GetAltitude()
            playerPitchForRangeData = PlayerUnit:GetPitch()
            playerHeadingForRangeData = PlayerUnit:GetHeading()
        end
    elseif EventData.IniUnit:GetCoalitionName() == "Red" then
     
       end
end
X_Airstrip:SetAutosaveOn()
X_Airstrip:Start()
