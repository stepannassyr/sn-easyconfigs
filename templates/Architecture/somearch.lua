-- Terminal colors
local colors = require 'ansicolors'

-------------------------------------------------------------------
-- Set architecture, systemname and prefix
-------------------------------------------------------------------
local architecture = myModuleVersion()
local systemname = ""
local quiet = architecture:sub(1,1) == "."
if architecture == ".Cortex-A72" then
    architecture = "Cortex-A72"
elseif architecture == ".Cortex-A76" then
    architecture = "Cortex-A76"
elseif architecture == ".Kunpeng920" then
    architecture = "Kunpeng920"
elseif architecture == ".Haswell" then
    architecture = "Haswell"
elseif architecture == ".ThunderX2" then
    architecture = "ThunderX2"
elseif architecture == ".Piledriver" then
    architecture = "Piledriver"
elseif architecture == ".Zen" then
    architecture = "Zen"
elseif architecture == ".Zen2" then
    architecture = "Zen2"
end

if architecture == "Cortex-A72" then
    systemname = "juaweihi1616"
elseif architecture == "Kunpeng920" then
    systemname = "juaweihi1620"
elseif architecture == "Haswell" then
    systemname = "haswell"
elseif architecture == "ThunderX2" then
    systemname = "tx2"
elseif architecture == "Piledriver" then
    systemname = "bd2"
elseif architecture == "Zen" then
    systemname = "zn1"
elseif architecture == "Zen2" then
    systemname = "zn2"
else
    LmodError("Trying to load an unsupported architecture!")
end

local prefix = os.getenv("SOFTWAREPREFIX")

-------------------------------------------------------------------
-- Module help and whatis
-------------------------------------------------------------------
help([[  This module will reset your module environment to use the ]] .. architecture .. [[ architecture ]])

whatis([[  Module to set up the environment for the ]] .. architecture .. [[ architecture ]])

-------------------------------------------------------------------
-- Get loaded stage and verify compatibility
-------------------------------------------------------------------
local stage = os.getenv("STAGE")

if stage == nil then
    stage = "current"
end

--if (stage == "Stage1" or stage == "Stage2" or stage == "2016a" or stage == "2016b") and 
--    (architecture == "KNL" or architecture == ".KNL") then
--    LmodError("\027[00;31mThe loaded stage is incompatible with the "..architecture.." architecture\027[00m")
--end
--if architecture == "KNL" then
--    conflict("Stages/2015a","Stages/2015b","Stages/2016a","Stages/2016b","Stages/Legacy")
--end

if not isloaded("Developers") then
    if isloaded("Stages") then
        LmodError("Loading this module while having the Stages module loaded might result in a broken environment!")
    end
end
-------------------------------------------------------------------
-- Set architecture path
-------------------------------------------------------------------
local software_root = pathJoin(prefix, systemname)

-------------------------------------------------------------------
-- Set path to other stages appropriately
-------------------------------------------------------------------
setenv("OTHERSTAGES", pathJoin(software_root, 'OtherStages'))

-------------------------------------------------------------------
-- Export architecture, architecture path and new Lmod system name
-------------------------------------------------------------------
old_software_root = os.getenv("SOFTWAREROOT") or ""
old_systemname = os.getenv("LMOD_SYSTEM_NAME") or ""
if mode()=="load" and not quiet then
    LmodMessage(colors("%{green}New $SOFTWAREROOT: ")..software_root.."\n"..
                colors("%{green}New $LMOD_SYSTEM_NAME: ")..systemname.."\n"..
                colors("%{green}New $ARCHITECTURE: ")..architecture
                )
end
setenv("SOFTWAREROOT", software_root)
setenv("ARCHITECTURE", architecture)
setenv("LMOD_SYSTEM_NAME", systemname)

-------------------------------------------------------------------
-- Set new cache
-------------------------------------------------------------------
setenv("LMOD_RC", pathJoin(software_root, "configs/lmodrc.lua"))

-------------------------------------------------------------------
-- Get $MODULEPATH, find old prefix, and "brute force" the new paths in
-------------------------------------------------------------------
local old_modulepath = os.getenv("MODULEPATH")

if old_software_root == nil or old_software_root == "" then
    for i in string.gmatch(old_modulepath, "([^:]+)") do
        -- This assumes that the prefix is in /usr/local/software
        tmp_system_prefix = {}
        for j in string.gmatch(i, "([^/]+)") do
            tmp_system_prefix[#tmp_system_prefix+1]=j
        end
        rootfound = false
	for pathindex=1,8 do
            old_systemname = tmp_system_prefix[pathindex] or ""
            if old_systemname == "juaweihi1616" or
               old_systemname == "juaweihi1620" or
               old_systemname == "haswell" or
               old_systemname == "tx2" or
               old_systemname == "zn1" or
               old_systemname == "zn2" then
                old_software_root = pathJoin(prefix, old_systemname)
                rootfound = true
                break
            end
        end
        if rootfound then
            break
        end
    end
end

if old_software_root == nil or old_software_root == "" then
    LmodWarning("I can't find the correct module paths to swap")
else
    local new_modulepath = string.gsub(old_modulepath, old_software_root, software_root)
    if mode()=="load" and not quiet then
        LmodMessage(colors("%{green}Re-setting $MODULEPATH to: "))
        LmodMessage(new_modulepath)
        LmodMessage(colors("%{red}Was: "))
        LmodMessage(old_modulepath)
end

-- Pushenv doesn't work when loading repeatedly the same module, lmod loses track of packages
if mode()=="load" then
    setenv("MODULEPATH", new_modulepath)
end
end

-------------------------------------------------------------------
-- Reload the developers module, if it was loaded, to trigger the setting of correct parameters
-------------------------------------------------------------------
if mode()=="load" then
    if isloaded("Developers") then
        load("Developers")
    end
end

-------------------------------------------------------------------
-- load arm optimized routines
-------------------------------------------------------------------
if mode() == "load" then
    if architecture == "Cortex-A72" or architecture == "Kunpeng920" or architecture == "ThunderX2" then
        load("arm-optimized-routines")
    end
end
-------------------------------------------------------------------
-- Print a warning
-------------------------------------------------------------------
if mode()=="load" and not quiet then
    LmodMessage(colors("%{red}\nWARNING: "..
                "%{yellow}Unloading this module might result in a broken environment. Please swap the module to use "..
                "the desired architecture instead.\n"
               ))
end


-------------------------------------------------------------------
-- Make the module sticky
-------------------------------------------------------------------
add_property("lmod", "sticky")
