local config = {}

local path_prj = ngx.var.PATH_PRJ
    or '/home/sites/pareto'
local filename = path_prj .. '/../etc/lua.conf'
local fh = assert(io.open(filename, 'r'))
for line in fh:lines() do
    line = line:gsub('^%s*','')
    line = line:gsub('%s*$','')
    if line ~= '' and not line:match('^[;#]') then
        local name, value = line:match('^(.-)%s*=%s*(.*)$')
        value = value:gsub('"([^"]*)"', '%1')
        value = value:gsub("'([^']*)'", '%1')
        value = value:gsub("$([%w_]+)", config)
        value = value:gsub("${([%w_]+)}", config)
        config[name] = value
    end
end

return config
