# CHANGELOG

## version 0.1.1

This is the very first version of lihil, but we already have a working version that users can play alon..

### Features

- core functionalities to an ASGI webserver, routing, http methods, `GET`, `POST`, `PUT`, `DELTE`
- ASGI middleware support
- variosu response and encoding supoprt, json response, text response, stream response, etc.
- bulitin json serialization/deseriazation using `msgspec`
- `CustomEncoder` and `CustomDecoder` support
- Performant and powerful dependency injection using `ididi`
- Builtin message support, `EventBus` that enables user to publish events to multiple listenrs.
- auto generated openapi shemas and swagger web-ui documentation
- rfc-9457 problem details and problems web-ui documentation
- many other things, stay tune to our docs!

## version 0.1.2

### Improvements

- `InvalidRequestErrors` is now a sublcass of `HTTPException`

### Fix

- fix a bug where `problem.__name__` is used for search param instead of `problem.__problem_type__`
- no longer import our experimental server by default

## version 0.1.3

### Fix

- fix a bug where if lifespan is not provided, callstack won't be built
- remove `loguru.logger` as dependency.

### Improvements

- `static` now works with `uvicorn`