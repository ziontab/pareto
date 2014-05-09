module('lib.api', package.seeall)

local cjson = require "cjson"
local utils = require "lib.utils"

function callback(self, json)
    if ngx.var.arg_callback then
        json = utils.unescape_uri(ngx.var.arg_callback) .. "(" .. json .. ")"
    end
    return json
end

function error_handle(self, error_code, msg)
    ngx.status = ngx.HTTP_INTERNAL_SERVER_ERROR
    ngx.say(self:callback(cjson.encode({
        status = "fail",
        code   = error_code,
        msg    = msg
    })))
end

function response_handle(self, data)
    ngx.say(self:callback(cjson.encode({
        status = "ok",
        data   = data
    })))
end

function response_ok(self)
    ngx.say(self:callback(cjson.encode({ status = "ok" })))
end
