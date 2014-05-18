local api = require "lib.api"
local cmd = require "lib.command"

local args = {}
function validate_params_est()
    if not args["name"] then
        api:error_handle(1, "invalid name")
        return 1
    end
    if not (args["id"] and string.match(args["id"], "^%d+$")) then
        api:error_handle(2, "invalid id")
        return 1
    end
    if not (args["data"]) then
        api:error_handle(3, "missed data")
        return 1
    end
    if not cmd:get(args["type"], args["name"]) then
        api:error_handle(4, "invalid criteria")
        return 1
    end
end

function validate_params_calc()
    if not (args["id"] and string.match(args["id"], "^%d+$")) then
        api:error_handle(2, "invalid id")
        return 1
    end
end

function validate_params_anal()
    if not (args["id"] and string.match(args["id"], "^%d+$")) then
        api:error_handle(2, "invalid id")
        return 1
    end
end

if ngx.req.get_method() ~= "POST" then
    api:error_handle(5, "invalid method")
    return 1
end

ngx.req.read_body()
args = ngx.req.get_post_args()

if not args["type"] then
    api:error_handle(6, "no type")
    return
end

if args["type"] == "calculation" then
    if validate_params_calc() then
        return
    end
elseif args["type"] == "estimation" then
    if validate_params_est() then
        return
    end
elseif args["type"] == "analysis" then
    if validate_params_anal() then
        return
    end
else
    api:error_handle(7, "invalid type")
    return
end

api:response_ok()

local function timer_handler(premature, type, name, data, id)
    local result, time = cmd:execute(cmd:get(type, name), data, id)
    cmd:set_result(type, id, result, time)
end

local ok, err = ngx.timer.at(0, timer_handler, args["type"],
                                args["name"], args["data"], args["id"])
if not ok then
    ngx.log(ngx.ERR, "failed to create timer: ", err)
    return
end
