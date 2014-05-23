module('lib.command', package.seeall)

local http   = require "resty.http"
local utils  = require "lib.utils"
local config = require "lib.config"
local cjson  = require "cjson"

function get_from_api(self, type, key)
    if type == "calculation" then
        if config.is_test_server then
            return "ps aux | grep calculation"
        else
            local id, algorithm, problem = string.match (key, "^(%d+):(%w+):(%w+)$")
            return "/root/i.shibitov/distribution/distribution_final -t "
            .. problem .. " -a " .. algorithm .. " -f /tmp/front_"
            .. id .. ".txt -i /tmp/indicators_" .. id .. ".txt"
        end
    elseif type == "estimation" then
        if key == "hv" then
            return "ps aux | grep hv"
        elseif key == "pvc" then
            return "ps aux | grep pvc"
        end
    end
    return
end


function get(self, type, raw_key)
    local key  = raw_key or ''
    local dict = ngx.shared.commands
    local name = dict:get(type .. ":" .. key)
    if not name then
        name = self:get_from_api(type, key)
        if name then
            dict:set(type .. ":" .. key, name)
        end
    end
    if not name then
        ngx.log(ngx.ERR, "No criteria: ", type, " ", key)
    end
    return name
end

function prepare(self, command, data, calc_id)
    -- load data into file
    return command
end

function _read_from(file)
    local f = io.open(file, "rb")
    if not f then
        ngx.log(ngx.ERR, "failed to open file: ", file)
        return ""
    end
    local content = f:read("*all")
    f:close()
    return content
end

function execute(self, command, type, id, data)
    local cmd = self:prepare(command, type, id)
    local file = "/tmp/result_" .. id
    local time1 = os.clock()
    os.execute("sleep 4")
    os.execute(cmd .. " > " .. file)
    local time2 = os.clock()
    local result
    if type == "calculation" then
        tmp = {}
        tmp["output"]    = _read_from(file)
        tmp["front"]     = _read_from("/tmp/front_" .. id)
        tmp["indicator"] = _read_from("/tmp/indicators_" .. id)
        result = cjson.encode(tmp)
    else
        result = _read_from(file)
    end
    return result, math.floor((time2 - time1) * 1000)
end

function set_result(self, type, id, result, time)
    local hc = http:new()
    local params = {
        type   = type,
        id     = id,
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
