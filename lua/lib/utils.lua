module('lib.utils', package.seeall)

local urllib = require "resty.url"

local function hex_to_char(x)
    return string.char(tonumber(x, 16))
end

function unescape_uri(url)
    return url:gsub("%%(%x%x)", hex_to_char)
end

function build_query(form)
    local kv = {}
    for k, v in pairs(form) do
        kv[#kv+1] = urllib.escape(k) .. '=' .. urllib.escape(v)
    end
    return table.concat(kv, '&')
end
