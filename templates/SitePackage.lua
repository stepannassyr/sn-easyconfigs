require("strict")
color = require("ansicolors")
local hook = require("Hook")

local swroot = os.getenv("SOFTWAREROOT")

-- Check if / is last character
if(swroot:sub(-1) == '/') then
  swroot = swroot:sub(1,swroot:len()-1)
end

-- remove last path component
local last
for cpt in swroot:gmatch("/[^/]*") do
  last = cpt
end
local gswroot = swroot:gsub(last,'',1)

local mapT =
{
   en_grouped = {
      ['/usr/lmod/lmod/modulefiles/Core$']     = "Core Modules",
      [gswroot..'/modulefiles/system$']        = "System modules",
      [gswroot..'/arm/modulefiles$']           = "ARM software",
      [gswroot..'/modules/system']             = "Architectures",
      [swroot..'/Stages/2019b/UI/Tools']       = "Core Modules",
      [swroot..'/Stages/2019b/UI/Compilers']   = "Compilers",
      [swroot..'/Stages/2019b/modules/all/Compiler/GCCcore/9%.2%.0']           = "Modules compiled with GCC 9.2.0",
      [swroot..'/Stages/2019b/modules/all/Compiler/GCC/9%.2%.0']               = "Modules compiled with GCC 9.2.0",
      [swroot..'/Stages/2019b/modules/all/Compiler/mpi/GCC/9%.2%.0']           = "MPI runtimes available for GCC 9.2.0",
      [swroot..'/Stages/2019b/modules/all/MPI/GCC/9%.2%.0/OpenMPI/4%.0%.2']    = "Modules built with GCC 9.2.0 and OpenMPI 4.0.2",
      [swroot..'/Stages/2019b/modules/all/MPI/armhpc/19%.2/OpenMPI/4%.0%.2']   = "Modules built with ARM compiler for HPC 19.2 and OpenMPI 4.0.2",
      [swroot..'/Stages/2019b/modules/all/Compiler/armhpc/19%.3']              = "Modules compiled with ARM compiler for HPC 19.3",
      [swroot..'/Stages/2019b/modules/all/Compiler/mpi/armhpc/19%.3']          = "MPI runtimes available for ARM compiler for HPC 19.3",
      [swroot..'/Stages/2019b/modules/all/MPI/armhpc/19%.3/OpenMPI/4%.0%.2']   = "Modules built with ARM compiler for HPC 19.3 and OpenMPI 4.0.2",
      [swroot..'/Stages/2019b/modules/all/Compiler/Clang/9%.0%.0']             = "Modules compiled with Clang 9.0.0",
      [swroot..'/Stages/2019b/modules/all/Compiler/mpi/Clang/9%.0%.0']         = "MPI runtimes available for Clang 9.0.0",
      [swroot..'/Stages/2019b/modules/all/MPI/Clang/9%.0%.0/OpenMPI/4%.0%.2']  = "Modules built with Clang 9.0.0 and OpenMPI 4.0.2",

   }
}

function avail_hook(t)
   LmodMessage("\n\n")
   LmodMessage(color("Load a compiler and MPI environment to make all Software for this combination available:\n\n\n\
      module load %{bright green blackbg}GCC %{bright yellow blackbg}OpenMPI%{reset}\n\n\n\
Please contact %{bright yellow blackbg}name@domain.com%{reset} if you require additional software."))
   LmodMessage("\n")
   local availStyle = masterTbl().availStyle
   local styleT     = mapT[availStyle]
   if (not availStyle or availStyle == "system" or styleT == nil) then
      return
   end

   for k,v in pairs(t) do
      for pat,label in pairs(styleT) do
         if (k:find(pat)) then
            t[k] = color("%{cyan bright blackbg}" .. label)
            break
         end
      end
   end
end

hook.register("avail",avail_hook)

