local api = require "lib.api"
local cmd = require "lib.command"

local command
if ngx.req.get_method() ~= "POST" then
    api:error_handle(5, "invalid method")
    return 1
end

ngx.req.read_body()
local args = ngx.req.get_post_args()

function validate_params()

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

    command = cmd:get(args["name"])
    if not command then
        api:error_handle(4, "invalid criteria")
        return 1
    end
end

if validate_params() then
    return
end

api:response_ok()
-- response stop
ngx.eof()

-- calulation
local result, time = cmd:execute(command, args["data"], args["id"])
cmd:set_result(args["id"], result, time)
