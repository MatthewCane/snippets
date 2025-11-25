from dns import resolver

DOMAIN = "current.cvd.clamav.net"

clamav_version = (
    resolver.resolve(DOMAIN, "TXT").response.answer[0][0].to_text().strip('"')
)

print(clamav_version)
