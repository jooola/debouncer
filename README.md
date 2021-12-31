# Debouncer

`Debouncer` is a proxy that debounce requests.

[![](https://mermaid.ink/svg/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgYyBhcyBDbGllbnRcbiAgICBwYXJ0aWNpcGFudCBmIGFzIEZ1bm5lbFxuICAgIHBhcnRpY2lwYW50IHMgYXMgU2VydmVyXG5cbiAgICBjLT4-ZjogTmV3IHJlcXVlc3RcbiAgICBhY3RpdmF0ZSBmXG5cbiAgICBmLT4-czogRGlzcGF0Y2ggcmVxdWVzdFxuICAgIFxuICAgIGFsdCB3aGVuIFRpbWVvdXQgPiAwXG4gICAgICAgIGYtPj5mOiBXYWl0IHJlcXVlc3QgdGltZW91dFxuICAgICAgICBjLS0-PmY6IDJuZCByZXF1ZXN0IChpZ25vcmVkIHdoZW4gdGltZW91dCBub3QgZWxhcHNlZClcbiAgICBlbHNlIHdoZW4gZm9yY2luZyByZXF1ZXN0IGRlbGV0aW9uIFxuICAgICAgICBzLT4-ZjogRm9yY2UgZGVsZXRlIHJlcXVlc3RcbiAgICBlbmRcblxuICAgIGYtPj5mOiBEZWxldGUgcmVxdWVzdFxuXG4gICAgZGVhY3RpdmF0ZSBmXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid.live/edit/#eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgYyBhcyBDbGllbnRcbiAgICBwYXJ0aWNpcGFudCBmIGFzIEZ1bm5lbFxuICAgIHBhcnRpY2lwYW50IHMgYXMgU2VydmVyXG5cbiAgICBjLT4-ZjogTmV3IHJlcXVlc3RcbiAgICBhY3RpdmF0ZSBmXG5cbiAgICBmLT4-czogRGlzcGF0Y2ggcmVxdWVzdFxuICAgIFxuICAgIGFsdCB3aGVuIFRpbWVvdXQgPiAwXG4gICAgICAgIGYtPj5mOiBXYWl0IHJlcXVlc3QgdGltZW91dFxuICAgICAgICBjLS0-PmY6IDJuZCByZXF1ZXN0IChpZ25vcmVkIHdoZW4gdGltZW91dCBub3QgZWxhcHNlZClcbiAgICBlbHNlIHdoZW4gZm9yY2luZyByZXF1ZXN0IGRlbGV0aW9uIFxuICAgICAgICBzLT4-ZjogRm9yY2UgZGVsZXRlIHJlcXVlc3RcbiAgICBlbmRcblxuICAgIGYtPj5mOiBEZWxldGUgcmVxdWVzdFxuXG4gICAgZGVhY3RpdmF0ZSBmXG4iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGVmYXVsdFwiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

## Config

To configure `Debouncer`, you can set the following environment variables:

```sh
# Path to the key/value store, default is "debouncer.db"
STORE_PATH=your-app.db
# Port for the http server, default is "4000"
PORT=8000
# Auth key for a key based auth, default is not set
AUTH_KEY=your-secret-auth-key
```

# Release

To release a new version, first bump the version number in `pyproject.toml` by hand or by using:

```sh
# poetry version --help
poetry version <patch|minor|major>
```

Make a release:

```sh
make release
```

Finally, push the release commit and tag to publish them to Pypi:

```sh
git push --follow-tags
```
