On game authentication, a 32-bit FRV-0 hash is computed and compared with a server-provided array for these files:

```
Data/Resources/DynamicMenuGroupDefs.json
Data/Resources/DynamicMenuIODefs.json
Data/Resources/WorldQuestDefs.json
Data/Resources/Persistent.lua
Data/Resources/Constellations.json
Data/Resources/AchievementDefs.json
Data/Resources/OutfitDefs.json
Data/Resources/StreamableDefs.lua
Data/Resources/NpcDefs.json
Data/Resources/SoundDefs.lua
Data/Resources/DailyQuestDefs.json
Data/Resources/ImageDefs.lua
Data/Resources/Boot.lua
Data/Resources/Seasons.json
Data/Resources/CollectibleDefs.json
```

Notice that the major Lua files are hit - except one, which is Data/Vars/Vars_Live.lua. If you want to hook into the game,
scan the global metatable, etc., this would be your way in. You can exec other Lua files with the `debugdofile(filename)` function.
