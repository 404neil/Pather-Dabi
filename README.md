# Pather Dabi

A community map for local reports and calls for help. It is one HTML file: no server, no accounts, no sign-up. Posts travel over [Nostr](https://nostr.com) relays, and phones can also pass updates to each other directly when the internet is down.

> **Status: early prototype.** The code was built and checked in a sandbox. The location rule, camera scanning and phone-to-phone sync still need testing on real devices. **Pather Dabi is not an emergency service. Always contact the police, ambulance or fire service first.**

## What it does

- **Map views:** Satellite, Relief, Physical and Street, with the India outline drawn on top as a gold line.
- **Pins:** Users choose their own heading (flood, road blocked, ...) and add a comment. Headings are lowercased and trimmed, and the app suggests ones already in use.
- **HELP NEEDED:** A reserved heading with big red markers and its own tab.
- **Verification:** Anyone can 👍/👎 and comment on a pin. Tapping the poster's name shows their profile.
- **Profiles and follows:** Display name and bio, follow/unfollow, and follow by QR code.
- **Chats:** Encrypted direct messages and group chats. Sharing a pin into a chat is one tap.
- **Offline:** Posts made without internet are saved on the device and sent later. Two phones on the same Wi-Fi or hotspot can swap updates by scanning QR codes (WebRTC), or by exporting and importing a file.
- **Relays:** Users can switch relays on and off and add their own `wss://` relay.
- **Guide tab:** Plain-language instructions inside the app.

## Rules

| | Rule |
|---|---|
| Posting | Only within **10 km of the poster's own device location** |
| Regular pin | Lasts 2 hours, or 24 hours once it has more than 10 upvotes. Removed at a net score of −3 or lower |
| HELP NEEDED pin | Lasts 12 hours. Votes don't change that |
| Deleting | Authors can delete their own pins at any time |
| Messages | Disappear after 24 hours |
| Group chat | Every member must follow every other member. If someone unfollows, the group pauses |
| Voting | Authors can't vote on their own pins |

## Quick start

1. **Open `index.html`** in a modern phone or desktop browser. Maps and relays need internet.
2. In the **Me** tab, set a display name and use **Back up key**. Your account is a key stored in the browser, so losing it means losing your pins and chats.
3. **Host or share it:**
   - Put the file in a GitHub repository and turn on GitHub Pages, or
   - send the file itself to people; it works without hosting.
4. Browsers can limit camera and location access on pages opened from a file, and some only allow them on `https` pages. If the camera won't open, use **Load photo of QR** (take a picture with the normal camera app, then pick it). If location is blocked, hosting the page on `https` usually fixes it.

## How it works

All data is signed [Nostr](https://github.com/nostr-protocol/nips) events, tagged `pather-dabi-v1` so they stay separate from other Nostr traffic.

| Data | Event kind |
|---|---|
| Pin (replaceable; deletion replaces it with an empty marker) | 30078 |
| Vote (`+` / `-`) | 7 |
| Comment | 1 |
| Profile | 0 |
| Follow list | 3 |
| Messages | 1059 gift wrap → 13 seal → 14 message, encrypted with NIP-44, in the style of NIP-17 |

Each client works out lifespans and vote tallies itself from the events it can see, so two users on different relays can briefly disagree. Every event's signature is checked before it is used, including events received from other phones.

**Sync:** Phone A shows a QR code, phone B scans it and shows a reply code, and A scans that. The phones then compare the events they hold, swap what's missing and later pass them to relays. No internet is needed, but both phones must be on the same Wi-Fi or hotspot.

## The 10 km location rule: what it does and doesn't do

Before posting, the app reads the device's location and only accepts pins inside a 10 km circle around it. The location is used on the device and is never posted.

This is a **deterrent, not a security guarantee**. Location is reported by the device and can be faked, and a modified client can skip the check. Other users can't prove where a poster was. The app relies on the community: votes, comments, and checking the poster's profile.

## Map data and the India outline

- The outline in `data/india-boundary.geojson` comes from [azaadshatru/OSM](https://github.com/azaadshatru/OSM) (OpenStreetMap data), simplified with a tolerance of about 0.004° (roughly 400 m). **Compare it with the Survey of India's official depiction before relying on it.**
- It's embedded in `index.html`. You can swap it: replace the data file and rebuild, paste GeoJSON into `EMBEDDED_BOUNDARY`, or use **Settings → Load India boundary file**.
- Satellite, Relief, Physical and Street tiles come from Esri. They draw no (or their own) boundary lines under the gold one; Street maps do show their own. Check [Esri's terms](https://www.esri.com/en-us/legal/terms/full-master-agreement) for your use.

## Build from source

The shipped `index.html` has Leaflet, the Nostr and QR libraries, and the boundary inlined, so it opens with no internet (apart from tiles and relays).

```
npm install
python3 tools/build.py      # writes index.html and THIRD-PARTY-NOTICES.md
```

- `src/app.html`: the application source (the build inlines the libraries and boundary)
- `data/india-boundary.geojson`: the simplified outline
- `tools/entry.js`, `tools/build.py`: bundling and assembly

To run your own network, change `APP` near the top of the script in `src/app.html`, and edit the default relay list there.

## Privacy and safety notes

- Pins, votes and comments are **public** and tied to a key, not a name.
- Messages are encrypted, but relays can still see who is messaging whom and when.
- Expiry and deletion are requests: relays aren't required to honor them.
- Anyone can create many keys, so votes can be gamed. Treat unverified pins with care.
- There is no moderation. Consider who runs the relays you use.

## Known limitations

Untested on real devices so far: WebRTC sync, camera and photo QR scanning, the 10 km check. QR codes for sync are dense and may need a few tries or the copy-and-paste option. Local storage caps how much a phone keeps (about 800 recent items). Street tiles stop at zoom 17. Offline, the map tiles are blank; pins, the boundary and lists still work.

## License

The original code, documentation and design of Pather Dabi are released under **[CC0 1.0 Universal](LICENSE)**: no rights reserved.

Not covered by CC0: the bundled libraries (Leaflet, nostr-tools, @noble/curves, @noble/hashes, @noble/ciphers, @scure/base, jsQR, qrcode-generator), which keep their MIT, BSD-2-Clause, Apache-2.0 or Unlicense terms, and the India outline data, which is © OpenStreetMap contributors under the ODbL. Full texts are in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) and inside `index.html`.
