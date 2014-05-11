module('lib.command', package.seeall)

local http   = require "resty.http"
local utils  = require "lib.utils"
local config = require "lib.config"

function get_from_api(self, key)
    if key == "hv" then
        return "ps aux | grep hv"
    elseif key == "pvc" then
        return "ps aux | grep pvc"
    end
    return
end


function get(self, raw_key)
    local key  = raw_key or ''
    local dict = ngx.shared.commands
    local name = dict:get(key)
    if not name then
        name = self:get_from_api(key)
        if name then
            dict:set(key, name)
        end
    end
    if not name then
        ngx.log(ngx.WARN, "No criteria: ", key)
    end
    return name
end

function prepare(self, command, data, calc_id)
    -- load data into file
    return command
end

function _read_from(file)
    local f = io.open(file, "rb")
    local content = f:read("*all")
    f:close()
    return content
end

function execute(self, command, data, calc_id)
    local cmd = self:prepare(command, data, calc_id)
    local file = "/tmp/result_" .. calc_id
    local time1 = os.clock()
    os.execute("sleep 4")
    os.execute(cmd .. " > " .. file)
    local time2 = os.clock()
    local result = _read_from(file)
    return result, math.floor((time2 - time1) * 1000)
end

function set_result(self, calc_id, result, time)
    local hc = http:new()
    local params = {
        id     = calc_id,
        data   = result,
        status = "ok",
        time   = time,
    }
    local ok, code, headers, status, body  = hc:request {
        url     = config.api_url,
        timeout = 3000,
        method  = "POST",
        headers = { ["Content-Type"] = "application/x-www-form-urlencoded" },
        body    = utils.build_query(params),
    }
    if code ~= 200 then
        ngx.log(ngx.ERR, status, body)
    end
end
