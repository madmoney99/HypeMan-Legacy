dofile('private_api_keys.lua')

print(PRIVATE_HYPEMAN_BOT_CLIENT_ID)
print(PRIVATE_HYPEMAN_CHANNEL_ID)

local BOT_CLIENT_ID = PRIVATE_HYPEMAN_BOT_CLIENT_ID
local CHANNEL_ID = PRIVATE_HYPEMAN_CHANNEL_ID


local dgram = require('dgram')
local discordia = require('discordia')

local client = discordia.Client()

client:on('ready', function()
    print('Logged in as '.. client.user.username)
end)

function readAll(file)
    local f = assert(io.open(file, "rb"))
    local content = f:read("*all")
    f:close()
    return content
end

client:on('messageCreate', function(message)	

	-- print('message received')
	--print(message.content)
	--if message.content == '!server_info' and message.channel.guild ~= nil then	

	if message.content == '!server_info' then
		local final_string = 'server_info.bat'
		os.execute(final_string)
		local str = readAll('server_info.txt')
		-- Disabled to remove duplicate mesages
		message.channel:send('```diff' .. str .. '```')
		return
	end

	if message.content == '#hypeman-help' then
		local helpstr = 'Boatstuff scoring:\n  "best": best trap of a calendar day (Default).\n  "first": first wire of the day, average of passes until you catch a wire. \n "20" last 20 passes by airframe. i.e. #hornet20 returns the last 20 passes of each pilot in the current month in the hornet. \n  Squadrons use will use first scoring.\n\nSquadrons:\n  Scans your DCS callsign for a squadron tag ie VFA-106.\n\nBoatstuff commands\n  #boatstuff (-first)\n  #turkeystuff (-first)\n  #scooterstuff (-first)\n  #goshawkstuff (-first)\n  #harrierstuff (-first)\n  #winderstuff\n  #checkmatestuff\n  #hornet20\n  #turkey20\n  #goshawk20\n\n Bomb and Strafe board commands:\n #bombboard\n #strafeboard'
		message.channel:send('```' .. helpstr .. '```')
	end
	
	if message.content == '#boatstuff -first' then
		local final_string = 'boardroom2.bat hornet first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}
		--channel.sendMessage("message").addFile(new File("path/to/file")).queue();
	end	
	
	if message.content == '#boatstuff' then
		local final_string = 'boardroom2.bat hornet'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}
		--channel.sendMessage("message").addFile(new File("path/to/file")).queue();
	end

	if message.content == '#turkeystuff -first' then
		local final_string = 'boardroom2.bat turkey first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end	
	
	if message.content == '#turkeystuff' then
		local final_string = 'boardroom2.bat turkey'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end
	

	if message.content == '#scooterstuff -first' then
		local final_string = 'boardroom2.bat scooter first'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end
	
	if message.content == '#scooterstuff' then
		local final_string = 'boardroom2.bat scooter'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end
	

	if message.content == '#winderstuff' then
		local final_string = 'boardroom2.bat hornet first vfa86'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end
	
	if message.content == '#checkmatestuff' then
		local final_string = 'boardroom2.bat turkey first vf211'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}		
	end	
	
	if message.content == '#harrierstuff' then
		local final_string = 'boardroom2.bat harrier'
		os.execute(final_string)
		message.channel:send {
			file = "final.jpg",
		}		
	end
	
	if message.content == '#goshawkstuff' then
		local final_string = 'boardroom2.bat goshawk'
		os.execute(final_string)		
		message.channel:send {
			file = "final.jpg",
		}			
	end
	if message.content == '#hornet20' then
		local final_string = 'boardroom20.bat hornet'
		os.execute(final_string)
		message.channel:send {
			file = "final.jpg",
		}		
	end
	if message.content == '#turkey20' then
		local final_string = 'boardroom20.bat turkey'
		os.execute(final_string)
		message.channel:send {
			file = "final.jpg",
		}		
	end
	if message.content == '#goshawk20' then
		local final_string = 'boardroom20.bat goshawk'
		os.execute(final_string)
		message.channel:send {
			file = "final.jpg",
		}		
	end
	
	if message.content == '#bombboard' then
		local final_string = 'boardroomRANGE.bat bomb'
		os.execute(final_string)		
		message.channel:send {
			file = "finalRange.jpg",
		}
	end
	
	if message.content == '#strafeboard' then
		local final_string = 'boardroomRANGE.bat strafe'
		os.execute(final_string)		
		message.channel:send {
			file = "finalRange.jpg",
		}		
	end
end)

client:run(BOT_CLIENT_ID)
