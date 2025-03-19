# Sol-Ark Cloud API

This is a package that implements an API client for the Sol-Ark Cloud web site.
This is an undocumented API and may change at any point, but so far it's a
fairly standard REST API.

**This project is in no way affiliated with Sol-Ark or their excellent
equipment.**

This was built primarily for integration into Home Assistant.

Note that the way the Sol-Ark inverters upload means that the data is only
updated once every 5 minutes. If you want something faster, you'll need to
pursue attaching to the ports on the inverters themselves.

## Known Issues

1. Pagination of plants. If you have >100 plants, this won't see all of them.
2. The flow response has a commented out entry since I don't know what it is.
