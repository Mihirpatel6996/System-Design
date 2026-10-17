# Music Player System — Dependency-First Design Notes

> A readable reconstruction of the UML diagram, organized from the **bottom-level classes upward**.
>
> The goal is not only to document the classes, but also to explain **why each relationship exists**: association, aggregation, composition, inheritance (`is-a`), implementation, and dependency.

---

## 1. System Requirements

### Functional Requirements

1. User can play and pause songs.
2. User can create playlists.
3. User can add songs to playlists.
4. User can play an entire playlist:
   - Sequentially
   - Randomly
   - Using a custom ordering strategy
5. Application supports multiple output devices:
   - Bluetooth speaker
   - Wired speaker
   - Headphones
6. New output devices and new playlist-playing strategies should be easy to add.

### Non-Functional Requirements

1. The design should be scalable.
2. New output devices should be addable without heavily modifying existing code.
3. New ways of playing songs from a playlist should be addable without heavily modifying existing code.
4. High-level application code should not need to know the details of every device or playback algorithm.

---

# 2. Big-Picture Architecture

The system can be understood as these major areas:

```text
                         MusicPlayerApplication
                                  |
                                  v
                         MusicPlayerFacade
                         /       |       \
                        /        |        \
                       v         v         v
              PlaylistManager  AudioEngine  StrategyManager
                    |              |              |
                    v              v              v
                Playlist      Output Device    PlayStrategy
                    |              |           /    |    \
                    v              v          /     |     \
                  Song      DeviceManager   Sequential Random Custom
                                   |
                                   v
                            DeviceFactory
                                   |
                                   v
                         IAudioOutputDevice
                          /        |        \
                         /         |         \
                        v          v          v
                  Bluetooth     Wired      Headphones
                   Adapter      Adapter      Adapter
                       |           |            |
                       v           v            v
                    Bluetooth   Wired       Headphone
                       API       API           API
```

The important idea is:

```text
Application
    ↓
Facade
    ↓
Managers / Engines
    ↓
Abstractions
    ↓
Concrete implementations
    ↓
External/device-specific APIs
```

This is why the dependency-first order starts from the bottom.

---

# 3. Dependency-First Order

The classes are introduced in this order:

1. `DeviceType`
2. `StrategyType`
3. `Song`
4. `IAudioOutputDevice`
5. Device-specific APIs
6. Output-device adapters
7. `DeviceFactory`
8. `DeviceManager`
9. `AudioEngine`
10. `Playlist`
11. `PlaylistManager`
12. `PlayStrategy`
13. `SequentialPlayStrategy`
14. `RandomPlayStrategy`
15. `CustomPlayStrategy`
16. `StrategyManager`
17. `MusicPlayerFacade`
18. `MusicPlayerApplication`

Why this order?

For example:

```text
MusicPlayerFacade
    ↓ depends on
AudioEngine
    ↓ depends on
IAudioOutputDevice
    ↓ implemented by
BluetoothSpeakerAdapter
```

If we explain `MusicPlayerFacade` first, the reader has to jump backward to understand what `AudioEngine` and `IAudioOutputDevice` mean.

Dependency-first ordering avoids that.

---

# 4. `DeviceType`

## Purpose

`DeviceType` represents the supported categories of audio output devices.

```text
DeviceType
-------------------------
BLUETOOTH
WIRED
HEADPHONES
...
```

This is an enum/type rather than a class containing device behavior.

## Why it exists

Instead of passing strings such as:

```text
"bluetooth"
"wired"
"headphones"
```

the system can use:

```text
DeviceType.BLUETOOTH
DeviceType.WIRED
DeviceType.HEADPHONES
```

This makes the available device types explicit.

## Used by

- `DeviceFactory`
- `DeviceManager`
- `MusicPlayerFacade`

---

# 5. `StrategyType`

`StrategyType` identifies the playlist-playing algorithm that should be used.

```text
StrategyType
-------------------------
SEQUENTIAL
RANDOM
CUSTOM
```

## Meaning

### SEQUENTIAL

Play:

```text
Song 1 → Song 2 → Song 3 → Song 4
```

### RANDOM

Play songs in a random order.

### CUSTOM

Use a user/application-defined ordering mechanism.

## Used by

- `StrategyManager`
- `MusicPlayerFacade`

---

# 6. `Song`

`Song` is one of the core domain objects.

```text
Song
-------------------------
- title : String
- artist : String
- path : String
-------------------------
+ getTitle() : String
+ getArtist() : String
+ getPath() : String
```

The exact getter/setter methods can vary; the important attributes shown in the UML are:

- title
- artist
- path

## Why `Song` is a separate class

A song is used by many parts of the system:

```text
Song
 ├── Playlist
 ├── AudioEngine
 ├── MusicPlayerApplication
 └── Output-device adapters
```

Therefore, song information should not be duplicated inside every other class.

---

# 7. `IAudioOutputDevice`

This is an abstraction for anything that can receive audio.

```text
<<abstract / interface>>
IAudioOutputDevice
-------------------------
+ playAudio(song : Song)
```

The concrete device classes implement this abstraction.

```text
                 IAudioOutputDevice
                  /       |       \
                 /        |        \
                v         v         v
        Bluetooth      Wired     Headphones
         Adapter       Adapter      Adapter
```

## Why an abstraction?

Suppose `AudioEngine` directly depended on:

```text
BluetoothSpeakerAdapter
```

Then adding headphones would require changing `AudioEngine`.

Instead:

```text
AudioEngine
      |
      v
IAudioOutputDevice
      |
      +---- BluetoothSpeakerAdapter
      +---- WiredSpeakerAdapter
      +---- HeadphonesAdapter
```

Now `AudioEngine` only cares that:

> "I have an audio output device that can play a song."

It does not care which physical device it is.

This is an important scalability point in the design.

---

# 8. Device-Specific APIs

The UML contains separate API classes representing the lower-level APIs used by different physical output devices.

---

## 8.1 `BluetoothSpeakerAPI`

```text
BluetoothSpeakerAPI
-------------------------
+ playSoundViaBluetooth(data : String)
```

Its job is to represent the Bluetooth-specific API.

The rest of the application should not need to know how Bluetooth playback works internally.

---

## 8.2 `WiredSpeakerAPI`

```text
WiredSpeakerAPI
-------------------------
+ playSoundViaCable(data : String)
```

This represents the lower-level wired-speaker API.

---

## 8.3 `HeadphoneAPI`

```text
HeadphoneAPI
-------------------------
+ playSoundViaJack(data : String)
```

This represents the lower-level headphone API.

---

# 9. Output Device Adapters

The UML uses adapter classes between the application's common interface and device-specific APIs.

This is the **Adapter Pattern** part of the design.

---

## 9.1 `BluetoothSpeakerAdapter`

```text
BluetoothSpeakerAdapter
-------------------------
- bluetoothSpeakerAPI : BluetoothSpeakerAPI
-------------------------
+ playAudio(song : Song)
```

It implements:

```text
IAudioOutputDevice
```

and internally uses:

```text
BluetoothSpeakerAPI
```

### Relationship

```text
BluetoothSpeakerAdapter
        |
        | implements
        v
IAudioOutputDevice

BluetoothSpeakerAdapter
        |
        | uses
        v
BluetoothSpeakerAPI
```

### Why Adapter is needed

The application expects:

```text
playAudio(Song)
```

But the Bluetooth API exposes something different:

```text
playSoundViaBluetooth(String)
```

The adapter translates between the two interfaces.

Conceptually:

```text
Application
    |
    | playAudio(song)
    v
BluetoothSpeakerAdapter
    |
    | converts song into required data
    v
BluetoothSpeakerAPI
    |
    | playSoundViaBluetooth(data)
    v
Bluetooth speaker
```

---

## 9.2 `WiredSpeakerAdapter`

```text
WiredSpeakerAdapter
-------------------------
- wiredSpeakerAPI : WiredSpeakerAPI
-------------------------
+ playAudio(song : Song)
```

Implements:

```text
IAudioOutputDevice
```

and uses:

```text
WiredSpeakerAPI
```

It translates:

```text
playAudio(Song)
```

into the wired API's required call.

---

## 9.3 `HeadphonesAdapter`

```text
HeadphonesAdapter
-------------------------
- headphoneAPI : HeadphoneAPI
-------------------------
+ playAudio(song : Song)
```

Implements:

```text
IAudioOutputDevice
```

and uses:

```text
HeadphoneAPI
```

---

# 10. Relationships in the Output Device Layer

## `BluetoothSpeakerAdapter` → `IAudioOutputDevice`

**Relationship: Realization / interface implementation**

Meaning:

```text
BluetoothSpeakerAdapter IS-A IAudioOutputDevice
```

because a Bluetooth adapter can be treated as an audio output device.

The same applies to:

```text
WiredSpeakerAdapter IS-A IAudioOutputDevice

HeadphonesAdapter IS-A IAudioOutputDevice
```

---

## Adapter → Device API

Example:

```text
BluetoothSpeakerAdapter → BluetoothSpeakerAPI
```

This is primarily a **dependency / has-a relationship**.

The adapter needs the API to perform its actual work.

It is not inheritance.

It means:

```text
BluetoothSpeakerAdapter HAS-A BluetoothSpeakerAPI
```

---

# 11. `DeviceFactory`

```text
DeviceFactory
-------------------------
+ createDevice(deviceType : DeviceType) : IAudioOutputDevice
```

## Purpose

Creates the correct output-device implementation.

Conceptually:

```text
createDevice(BLUETOOTH)
        ↓
BluetoothSpeakerAdapter

createDevice(WIRED)
        ↓
WiredSpeakerAdapter

createDevice(HEADPHONES)
        ↓
HeadphonesAdapter
```

## Why Factory?

Without a factory, higher-level code might contain:

```text
if type == BLUETOOTH
    create BluetoothSpeakerAdapter

else if type == WIRED
    create WiredSpeakerAdapter

else if type == HEADPHONES
    create HeadphonesAdapter
```

The creation logic would be spread into application classes.

With the factory:

```text
DeviceManager
      |
      v
DeviceFactory
      |
      +---- BluetoothSpeakerAdapter
      +---- WiredSpeakerAdapter
      +---- HeadphonesAdapter
```

The creation responsibility is centralized.

---

# 12. `DeviceManager`

The UML marks `DeviceManager` as a Singleton.

```text
<<Singleton>>
DeviceManager
-------------------------
- device : IAudioOutputDevice
-------------------------
+ connect(deviceType : DeviceType)
+ getDevice() : IAudioOutputDevice
```

## Responsibility

It manages the currently connected/selected output device.

Example:

```text
connect(BLUETOOTH)
```

may result in:

```text
DeviceFactory
      ↓
BluetoothSpeakerAdapter
      ↓
DeviceManager.device
```

Later:

```text
connect(HEADPHONES)
```

changes the current device.

---

## Relationship: `DeviceManager` → `IAudioOutputDevice`

The UML shows a diamond on the `DeviceManager` side.

That represents **composition** in the diagram.

Conceptually:

```text
DeviceManager
      ◆
      |
      v
IAudioOutputDevice
```

The intended meaning is that the manager owns/manages its current output-device reference.

### Important UML learning point

The diamond is about **lifecycle/ownership semantics**, not simply "this class has a field."

A field such as:

```text
IAudioOutputDevice device;
```

by itself does not automatically mean composition.

Composition means the containing object strongly owns the contained part.

In this particular design, the diagram is expressing strong ownership/management of the current device.

---

# 13. `AudioEngine`

```text
AudioEngine
-------------------------
- currentSong : Song
-------------------------
+ play(audio : IAudioOutputDevice, song : Song)
+ pause()
```

## Responsibility

`AudioEngine` coordinates actual playback.

It receives:

```text
IAudioOutputDevice
Song
```

and asks the device to play the song.

Conceptually:

```text
AudioEngine
     |
     | play(device, song)
     v
IAudioOutputDevice
     |
     v
Concrete Adapter
     |
     v
Device API
```

## Why does AudioEngine depend on the interface?

It should not need code such as:

```text
if Bluetooth
    ...
else if Wired
    ...
else if Headphones
    ...
```

Instead:

```text
audioDevice.playAudio(song)
```

works for every implementation.

This is one of the major extensibility points of the design.

---

# 14. `Playlist`

```text
Playlist
-------------------------
- name : String
- songs : Vector<Song>
-------------------------
+ addSong(song : Song)
+ get...()
+ set...()
```

The playlist contains multiple songs.

Conceptually:

```text
Playlist
    |
    +── Song
    +── Song
    +── Song
```

---

## Relationship: `Playlist` → `Song`

The UML shows a collection of songs and a `1..*` multiplicity.

That means a playlist can contain one or more songs in the intended model.

The relationship is best understood as:

```text
Playlist HAS-A collection of Songs
```

The exact choice between aggregation and composition depends on the intended lifecycle.

### Important distinction

A `Song` normally exists independently of a playlist.

For example:

```text
Song "Believer"
```

can exist in:

```text
Playlist A
Playlist B
Playlist C
```

and removing it from one playlist should not destroy the song.

Therefore, **conceptually this is better modeled as aggregation/association rather than composition** if the `Song` objects are shared independently.

If the diagram's filled diamond is intended to indicate composition, that is a stronger ownership claim and should only be used if the design intends the playlist to own the lifecycle of its `Song` objects.

For a real music-player domain model, keeping songs independent is generally the cleaner lifecycle interpretation.

---

# 15. `PlaylistManager`

The UML marks this class as a Singleton.

```text
<<Singleton>>
PlaylistManager
-------------------------
- playlists : Map<String, Playlist>
-------------------------
+ createPlaylist(name : String)
+ addSongToPL(playlistName : String, song : Song)
+ getPlaylist(name : String) : Playlist
```

## Responsibility

It manages all playlists.

Conceptually:

```text
PlaylistManager
      |
      +── "Workout" → Playlist
      +── "Favorites" → Playlist
      +── "Chill" → Playlist
```

The map allows a playlist to be found using its name.

---

## Relationship: `PlaylistManager` → `Playlist`

The UML shows a filled diamond on the `PlaylistManager` side.

That is **composition**.

```text
PlaylistManager
       ◆
       |
       v
   Playlist
```

The diagram therefore communicates:

> The `PlaylistManager` owns/manages the lifecycle of the playlists in its collection.

This is more defensible than composition between `Playlist` and `Song`, because the manager explicitly owns its collection of playlists.

---

# 16. `PlayStrategy`

This is an abstract strategy interface/base class.

```text
<<abstract>>
PlayStrategy
-------------------------
+ setPlaylist(playlist : Playlist)
+ hasNext() : boolean
+ next()
+ hasPrevious() : boolean
+ previous()
+ addToNext()
```

The exact return types can be refined during implementation; the important point is the common contract.

---

# 17. Why `PlayStrategy` Exists

The requirement says:

> A playlist can be played sequentially, randomly, or using a custom order.

These are different algorithms.

Instead of putting all algorithms into `Playlist`:

```text
Playlist
    if sequential...
    else if random...
    else if custom...
```

we create separate strategy classes.

```text
                 PlayStrategy
                <<abstract>>
                     △
             ________|________
            /        |        \
           /         |         \
          v          v          v
   Sequential     Random      Custom
```

This is the **Strategy Pattern**.

The rest of the application works with:

```text
PlayStrategy
```

rather than depending directly on every algorithm.

---

# 18. `SequentialPlayStrategy`

```text
SequentialPlayStrategy
-------------------------
- playlist : Playlist
- index : int
-------------------------
+ setPlaylist(playlist : Playlist)
+ hasNext()
+ next()
+ hasPrevious()
+ previous()
+ addToNext()
```

It plays songs in their playlist order.

Example:

```text
Playlist:

[ A, B, C, D ]

Sequential:

A → B → C → D
```

## Relationship

```text
SequentialPlayStrategy IS-A PlayStrategy
```

because it implements/extends the common strategy abstraction.

---

# 19. `RandomPlayStrategy`

```text
RandomPlayStrategy
-------------------------
- playlist : Playlist
-------------------------
+ setPlaylist(playlist : Playlist)
+ hasNext()
+ next()
+ hasPrevious()
+ previous()
+ addToNext()
```

Its job is to choose the next song using a random ordering.

Example:

```text
Playlist:

[ A, B, C, D ]

Possible playback:

C → A → D → B
```

## Relationship

```text
RandomPlayStrategy IS-A PlayStrategy
```

---

# 20. `CustomPlayStrategy`

```text
CustomPlayStrategy
-------------------------
- playlist : Playlist
-------------------------
+ setPlaylist(playlist : Playlist)
+ hasNext()
+ next()
+ hasPrevious()
+ previous()
+ addToNext()
```

Its job is to support a custom ordering algorithm.

For example:

```text
User-defined:

D → A → C → B
```

## Relationship

```text
CustomPlayStrategy IS-A PlayStrategy
```

---

# 21. Why Strategy Pattern Makes the System Scalable

Suppose tomorrow the application needs:

```text
REPEAT_ONE
SHUFFLE_WITHOUT_REPEAT
MOST_PLAYED_FIRST
RECENTLY_ADDED_FIRST
AI_RECOMMENDED
```

Without Strategy Pattern, the existing playback class could become a large collection of conditionals.

With Strategy Pattern:

```text
PlayStrategy
     |
     +── SequentialPlayStrategy
     +── RandomPlayStrategy
     +── CustomPlayStrategy
     +── RepeatOneStrategy
     +── ShuffleWithoutRepeatStrategy
     +── MostPlayedFirstStrategy
     +── AIRecommendedStrategy
```

The existing clients can continue using:

```text
PlayStrategy
```

without knowing which algorithm is being used.

---

# 22. `StrategyManager`

The UML marks this class as a Singleton.

```text
<<Singleton>>
StrategyManager
-------------------------
- sequentialStrategy : SequentialPlayStrategy
- randomStrategy : RandomPlayStrategy
- customQueueStrategy : CustomPlayStrategy
-------------------------
+ getStrategy(type : StrategyType) : PlayStrategy
```

## Responsibility

It provides the appropriate strategy.

Conceptually:

```text
getStrategy(SEQUENTIAL)
        ↓
SequentialPlayStrategy

getStrategy(RANDOM)
        ↓
RandomPlayStrategy

getStrategy(CUSTOM)
        ↓
CustomPlayStrategy
```

This centralizes strategy selection.

---

# 23. Relationship: `StrategyManager` → Strategies

The UML shows a filled diamond near `StrategyManager`.

The intended model is that `StrategyManager` owns/manages the strategy objects it provides.

```text
StrategyManager
       ◆
       |
       +── SequentialPlayStrategy
       +── RandomPlayStrategy
       +── CustomPlayStrategy
```

The manager can therefore act as a shared registry/provider of the available strategies.

---

# 24. `MusicPlayerFacade`

This is one of the most important classes.

The UML marks it as a Singleton.

```text
<<Singleton>>
MusicPlayerFacade
-------------------------
- audioEngine : AudioEngine
- currentPlaylist : Playlist
- strategy : PlayStrategy
-------------------------
+ connectDevice(deviceType : DeviceType)
+ setStrategy(type : StrategyType)
+ loadPlaylist(name : String)
+ playSong(song : Song)
+ pauseSong(song : Song)
+ playAll()
+ playNext()
+ playPrevious()
+ enqueueNext()
```

The exact method signatures can be adjusted during implementation, but the responsibilities shown in the diagram are centered around these operations.

---

# 25. Why `MusicPlayerFacade` Exists

The music-player application should not need to directly coordinate:

```text
DeviceManager
DeviceFactory
AudioEngine
PlaylistManager
StrategyManager
PlayStrategy
```

For example, without a facade, the application might need to do:

```text
playlistManager.getPlaylist(...)
strategyManager.getStrategy(...)
strategy.setPlaylist(...)
deviceManager.getDevice(...)
audioEngine.play(...)
```

That exposes too much internal complexity.

Instead:

```text
MusicPlayerApplication
          |
          v
   MusicPlayerFacade
```

The application can say:

```text
facade.loadPlaylist("Favorites")
facade.setStrategy(SEQUENTIAL)
facade.connectDevice(BLUETOOTH)
facade.playAll()
```

The facade coordinates the internal objects.

---

# 26. Facade Pattern

The `MusicPlayerFacade` is an example of the **Facade Pattern**.

It provides:

```text
Simple interface
      ↓
Complex subsystem
```

Specifically:

```text
MusicPlayerApplication
          |
          v
   MusicPlayerFacade
          |
    +-----+------+----------------+
    |            |                |
    v            v                v
Playlist      AudioEngine     StrategyManager
Manager                           |
                                  v
                            PlayStrategy
```

The application does not need to understand all subsystem details.

---

# 27. `MusicPlayerApplication`

This is the top-level application/client class.

The UML marks it as a Singleton.

```text
<<Singleton>>
MusicPlayerApplication
-------------------------
- songs : Vector<Song>
-------------------------
+ createSong(...)
+ createPlaylist(...)
+ addSong(...)
+ other application methods
```

The diagram also indicates that it calls into other classes to perform operations.

## Responsibility

This is the application-facing layer.

It can:

1. Maintain/create songs.
2. Create playlists.
3. Add songs to playlists.
4. Use the facade for playback-related operations.

---

# 28. Why `MusicPlayerApplication` Should Not Do Everything

A common beginner design is:

```text
MusicPlayerApplication
    |
    +-- create device
    +-- select device
    +-- play song
    +-- select strategy
    +-- manage playlist
    +-- implement random algorithm
    +-- call Bluetooth API
    +-- call wired API
```

That class becomes a **God Object**.

This UML avoids that by distributing responsibilities:

```text
MusicPlayerApplication
        ↓
MusicPlayerFacade
        ↓
   ┌────┼─────────────┐
   ↓    ↓             ↓
Playlist Audio       Strategy
Manager  Engine       Manager
          ↓             ↓
       Device       PlayStrategy
       System
```

---

# 29. Complete Relationship Map

## 29.1 Inheritance / IS-A relationships

```text
BluetoothSpeakerAdapter IS-A IAudioOutputDevice

WiredSpeakerAdapter IS-A IAudioOutputDevice

HeadphonesAdapter IS-A IAudioOutputDevice

SequentialPlayStrategy IS-A PlayStrategy

RandomPlayStrategy IS-A PlayStrategy

CustomPlayStrategy IS-A PlayStrategy
```

These are polymorphic relationships.

---

# 30. HAS-A / Association Relationships

Examples:

```text
AudioEngine HAS-A current Song/reference

Playlist HAS-A collection of Songs

PlaylistManager HAS-A collection/map of Playlists

MusicPlayerFacade HAS-A AudioEngine

MusicPlayerFacade HAS-A current Playlist

MusicPlayerFacade HAS-A PlayStrategy

DeviceManager HAS-A current IAudioOutputDevice

Adapters HAS-A their corresponding device API
```

A **has-a** statement describes the conceptual relationship.

It does not automatically mean UML aggregation or composition.

---

# 31. Composition Relationships

The UML uses filled diamonds to indicate strong ownership.

The important ones shown are:

```text
PlaylistManager ◆── Playlist

DeviceManager ◆── IAudioOutputDevice

StrategyManager ◆── Strategy implementations
```

### Meaning

The containing class is intended to own/manage the lifecycle of the object on the other side.

---

# 32. Aggregation vs Composition — Important Learning Note

These two are frequently confused.

## Aggregation

```text
Container ◇──── Part
```

Means:

> The container has parts, but the parts can meaningfully exist independently.

Example:

```text
Playlist ◇──── Song
```

A song can exist without a particular playlist.

---

## Composition

```text
Container ◆──── Part
```

Means:

> The part is strongly owned by the container and its lifecycle is tied to that container.

Example:

```text
PlaylistManager ◆──── Playlist
```

if the manager is responsible for creating and owning the playlists.

---

# 33. Dependency vs Association

Another important distinction:

## Dependency

A class temporarily needs another class to perform an operation.

Example:

```text
AudioEngine.play(IAudioOutputDevice device, Song song)
```

The engine depends on the device abstraction for that operation.

---

## Association

A class keeps a longer-lived reference to another object.

Example:

```text
MusicPlayerFacade
    - audioEngine : AudioEngine
```

The facade has a persistent reference to the engine.

---

# 34. Complete Dependency Graph

A simplified dependency graph is:

```text
DeviceType
     ↓
DeviceFactory
     ↓
IAudioOutputDevice
     ↑
     |
Concrete Adapters
     |
     +── BluetoothSpeakerAPI
     +── WiredSpeakerAPI
     +── HeadphoneAPI

DeviceManager
     ↓
IAudioOutputDevice


Song
 ↓
Playlist
 ↓
PlaylistManager


Playlist
 ↓
PlayStrategy
 ↑
 ├── SequentialPlayStrategy
 ├── RandomPlayStrategy
 └── CustomPlayStrategy
          ↑
          |
   StrategyManager


Song + IAudioOutputDevice
          ↓
     AudioEngine


AudioEngine
Playlist
PlayStrategy
          ↓
  MusicPlayerFacade
          ↓
MusicPlayerApplication
```

---

# 35. Design Patterns Used

The UML combines several design patterns.

| Pattern | Where | Purpose |
|---|---|---|
| Singleton | `MusicPlayerApplication` | Single application-level instance |
| Singleton | `MusicPlayerFacade` | Single facade instance |
| Singleton | `PlaylistManager` | Central playlist manager |
| Singleton | `DeviceManager` | Central device manager |
| Singleton | `StrategyManager` | Central strategy manager |
| Factory | `DeviceFactory` | Create correct output-device adapter |
| Adapter | Device adapters | Convert common audio interface to device-specific APIs |
| Strategy | `PlayStrategy` + implementations | Switch playlist playback algorithms |
| Facade | `MusicPlayerFacade` | Hide subsystem complexity |

---

# 36. Why These Patterns Work Together

These patterns solve different problems.

### Factory

Answers:

> "Which object should I create?"

```text
DeviceFactory
```

### Adapter

Answers:

> "How do I make different device APIs look the same?"

```text
IAudioOutputDevice
       ↑
Adapters
```

### Strategy

Answers:

> "Which playlist-playing algorithm should I use?"

```text
PlayStrategy
    ↑
Sequential / Random / Custom
```

### Facade

Answers:

> "How can the application use all these subsystems without knowing their internal details?"

```text
MusicPlayerFacade
```

### Singleton

Answers:

> "Should there be one shared manager/facade/application instance?"

```text
<<Singleton>>
```

---

# 37. Example: Playing a Song

Suppose the user selects Bluetooth output and plays a song.

The flow becomes:

```text
MusicPlayerApplication
        |
        v
MusicPlayerFacade
        |
        v
DeviceManager.connect(BLUETOOTH)
        |
        v
DeviceFactory
        |
        v
BluetoothSpeakerAdapter
        |
        v
BluetoothSpeakerAPI
```

Then playback:

```text
MusicPlayerFacade
        |
        v
AudioEngine.play(device, song)
        |
        v
IAudioOutputDevice.playAudio(song)
        |
        v
BluetoothSpeakerAdapter.playAudio(song)
        |
        v
BluetoothSpeakerAPI.playSoundViaBluetooth(data)
```

Notice that `AudioEngine` does not need to know that Bluetooth exists.

---

# 38. Example: Playing a Playlist Sequentially

Suppose:

```text
Playlist = [A, B, C]
```

The user selects sequential mode.

```text
MusicPlayerApplication
        |
        v
MusicPlayerFacade
        |
        +── loadPlaylist("My Playlist")
        |
        +── setStrategy(SEQUENTIAL)
                  |
                  v
          StrategyManager
                  |
                  v
        SequentialPlayStrategy
```

Then:

```text
SequentialPlayStrategy
        |
        | next()
        v
       A
        |
        | next()
        v
       B
        |
        | next()
        v
       C
```

The playback algorithm is separated from the playlist itself.

---

# 39. Example: Switching to Random Playback

The playlist does not change.

Only the strategy changes:

```text
Playlist
[A, B, C, D]
```

Change:

```text
SequentialPlayStrategy
```

to:

```text
RandomPlayStrategy
```

Now:

```text
A → B → C → D
```

could become:

```text
C → A → D → B
```

The `Playlist` class does not need to be modified.

This is exactly the kind of extensibility the Strategy Pattern is intended to provide.

---

# 40. Example: Adding a New Output Device

Suppose tomorrow we add:

```text
USB DAC
```

A scalable design should not require rewriting `AudioEngine`.

We can add:

```text
UsbDacAPI
```

then:

```text
UsbDacAdapter implements IAudioOutputDevice
```

and update the creation mechanism:

```text
DeviceFactory
    |
    +── Bluetooth
    +── Wired
    +── Headphones
    +── USB DAC
```

The core playback code can still use:

```text
IAudioOutputDevice.playAudio(song)
```

This demonstrates why programming against the abstraction is important.

---

# 41. Example: Adding a New Playback Strategy

Suppose a new requirement appears:

```text
MostPlayedFirstStrategy
```

Create:

```text
MostPlayedFirstStrategy
        |
        v
implements PlayStrategy
```

The existing architecture remains:

```text
MusicPlayerFacade
        ↓
PlayStrategy
        ↑
Sequential
Random
Custom
MostPlayedFirst
```

The new behavior is added as another implementation rather than modifying the existing strategies.

---

# 42. Why the Design Is Scalable

The design separates three areas that are likely to change independently.

## Area 1 — Output devices

```text
IAudioOutputDevice
        ↑
    adapters
        ↑
device-specific APIs
```

Adding a device means adding a new implementation.

---

## Area 2 — Playlist algorithms

```text
PlayStrategy
      ↑
implementations
```

Adding a new playback algorithm means adding another strategy.

---

## Area 3 — Application coordination

```text
MusicPlayerFacade
```

The facade keeps the application-facing interface stable while internal components evolve.

---

# 43. One Important Design Principle Behind the UML

A recurring principle throughout the design is:

> Depend on abstractions rather than concrete implementations.

For example:

Bad:

```text
AudioEngine
    ↓
BluetoothSpeakerAdapter
```

Better:

```text
AudioEngine
    ↓
IAudioOutputDevice
    ↑
BluetoothSpeakerAdapter
```

Similarly:

Bad:

```text
MusicPlayerFacade
    ↓
RandomPlayStrategy
```

Better:

```text
MusicPlayerFacade
    ↓
PlayStrategy
    ↑
RandomPlayStrategy
```

This allows the implementation behind the abstraction to change.

---

# 44. Dependency-First Summary

The final learning order is:

```text
LEVEL 1 — Basic types
    DeviceType
    StrategyType

LEVEL 2 — Core domain object
    Song

LEVEL 3 — Output abstraction
    IAudioOutputDevice

LEVEL 4 — External/device APIs
    BluetoothSpeakerAPI
    WiredSpeakerAPI
    HeadphoneAPI

LEVEL 5 — Adapter implementations
    BluetoothSpeakerAdapter
    WiredSpeakerAdapter
    HeadphonesAdapter

LEVEL 6 — Device creation
    DeviceFactory

LEVEL 7 — Device management
    DeviceManager

LEVEL 8 — Playback engine
    AudioEngine

LEVEL 9 — Playlist domain
    Playlist

LEVEL 10 — Playlist management
    PlaylistManager

LEVEL 11 — Playback abstraction
    PlayStrategy

LEVEL 12 — Playback strategies
    SequentialPlayStrategy
    RandomPlayStrategy
    CustomPlayStrategy

LEVEL 13 — Strategy management
    StrategyManager

LEVEL 14 — System coordination
    MusicPlayerFacade

LEVEL 15 — Application
    MusicPlayerApplication
```

This order means that every class can be understood using concepts that were already introduced.

---

# 45. Final Mental Model

Think about the system as five layers:

```text
┌───────────────────────────────────────┐
│          APPLICATION LAYER            │
│     MusicPlayerApplication             │
└───────────────────┬───────────────────┘
                    ↓
┌───────────────────────────────────────┐
│             FACADE LAYER              │
│       MusicPlayerFacade               │
└───────────────────┬───────────────────┘
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
┌────────────┐ ┌──────────┐ ┌──────────────┐
│ Playlist   │ │  Audio   │ │   Strategy   │
│ Management │ │  Engine  │ │  Management  │
└─────┬──────┘ └────┬─────┘ └──────┬───────┘
      ↓             ↓              ↓
   Playlist    IAudioOutput     PlayStrategy
      ↓             ↑              ↑
     Song        Adapters     Sequential/Random/
                    ↓          Custom strategies
                Device APIs
```

The key separation is:

```text
WHAT the system can do
        ↓
abstractions/interfaces

HOW a particular thing is done
        ↓
concrete implementations
```

That separation is what makes the design easier to extend.

---

# 46. Relationship Cheat Sheet

| Relationship | Meaning | Example in this system |
|---|---|---|
| `IS-A` | Inheritance/generalization | `RandomPlayStrategy` IS-A `PlayStrategy` |
| Implements | Concrete class fulfills an interface/abstract contract | `BluetoothSpeakerAdapter` implements `IAudioOutputDevice` |
| `HAS-A` | One object contains/uses another object | `MusicPlayerFacade` HAS-A `AudioEngine` |
| Association | Objects are related | `Playlist` associated with `Song` |
| Aggregation `◇` | Weak whole-part relationship; part can live independently | Suitable conceptual model for `Playlist` → `Song` when songs are independent |
| Composition `◆` | Strong ownership/lifecycle relationship | `PlaylistManager` → `Playlist` as drawn |
| Dependency | One class temporarily needs another to perform an operation | `AudioEngine` depends on `IAudioOutputDevice` to play |
| Realization | Class implements an interface/abstract contract | Device adapters → `IAudioOutputDevice` |

---

# 47. Final Architecture in One Diagram

```text
                         ┌────────────────────────┐
                         │ MusicPlayerApplication │
                         │      <<Singleton>>     │
                         └───────────┬────────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │   MusicPlayerFacade    │
                         │      <<Singleton>>     │
                         └───────┬────┬─────┬────┘
                                 │    │     │
                   ┌─────────────┘    │     └──────────────┐
                   ▼                  ▼                    ▼
          ┌────────────────┐  ┌──────────────┐  ┌────────────────┐
          │PlaylistManager │  │ AudioEngine  │  │StrategyManager │
          │  <<Singleton>> │  └──────┬───────┘  │  <<Singleton>> │
          └───────┬────────┘         │          └───────┬────────┘
                  │                  │                  │
                  ▼                  ▼                  ▼
              Playlist       IAudioOutputDevice     PlayStrategy
                  │                  ▲                  ▲
                  ▼                  │                  │
                Song         ┌───────┼────────┐    ┌────┼────────┐
                             │       │        │    │    │        │
                             ▼       ▼        ▼    ▼    ▼        ▼
                          Bluetooth Wired Headphones Seq  Random Custom
                           Adapter  Adapter Adapter
                              │       │        │
                              ▼       ▼        ▼
                          Bluetooth Wired  Headphone
                             API      API      API

                         DeviceManager
                         <<Singleton>>
                              │
                              ▼
                       DeviceFactory
                              │
                              ▼
                    creates device adapters
```

---

## 48. Core Takeaway

The design is not just a collection of classes.

Each major class has a reason to exist:

```text
Song
    → represents song data

Playlist
    → groups songs

PlaylistManager
    → manages playlists

IAudioOutputDevice
    → gives every output device a common contract

Adapters
    → make incompatible device APIs compatible

DeviceFactory
    → centralizes device creation

DeviceManager
    → manages the active output device

AudioEngine
    → performs playback through the abstraction

PlayStrategy
    → defines playlist traversal behavior

Concrete Strategies
    → implement sequential/random/custom behavior

StrategyManager
    → selects the required strategy

MusicPlayerFacade
    → hides subsystem complexity

MusicPlayerApplication
    → represents the application/client
```

The central architectural idea is:

```text
               CHANGE
                 │
       ┌─────────┴─────────┐
       │                   │
New output device     New playback algorithm
       │                   │
       ▼                   ▼
IAudioOutputDevice     PlayStrategy
       │                   │
    Adapter          New Strategy class
       │                   │
       └─────────┬─────────┘
                 ▼
         Existing high-level
             code remains
             mostly stable
```

That is the main reason this design satisfies the scalability requirement.
