# Report-Back (`reback`)

A simple utility that allows individual agents to report back to peers on the same broadcast network with basic metrics and information.

## Motivation

I've been in several spaces where keeping track of ad-hoc machines has been necessary. They change IPs, or people set static IPs without consulting, causing various issues.

Installing and setting up a full monitoring solution has not always been possibile. Sometimes the monitoring server itself has needed to be on a potentially transient IP.

This project aims to provide a lightweight solution to this type of issue.

## Listening Agent/Peer

Each agent broadcasts a single UDP packet periodically containing its hostname and currrent load, and optionally a tag string, from which other agents derive the IP and MAC. On receiving a pingout from any other agent (peers), a receiving agent records the information to stdout with a timestamp.

If a callback command is specified, it is called each time a new pingout is received (eventual duplicates are ignored). This can be useful for subsequently hooking into other systems.

```sh
reback start [OPTIONS ...] BROADCAST_IP
```

* `BROADCAST_IP` - the broadcast IP to send pingouts to
* `-p PORT` - the port to listen and broadcast on. All agents should use the same port
    * default `42324`
* `-Q QUERIES_PORT` - HTTP listener for queries
* `-T TAGS` - an agent can specify tags, in which case it will only record pingouts that carry at least one tag in common
    * default empty - agent sends no tags, and records all
* `-A` - record all, even if tags were specififed
    * default `false`
* `-P PERIODICITY` - how frequently to send a pingout, in seconds
    * default `30`
    * if `prime` is specified, uses a random choice from `17, 19, 23, 29, 31, 37, 41` (to be checked) (prime numbers)
    * if `random` is specified, chooses a new prime number from the above list after each pingout sent
* `-r RETAIN_COUNT` - retain last entry for `RETAIN_COUNT` number of peers
    * default `20`
* `-I INFO_SCRIPT` - path to a script to run when queried for information
    * default is to run `uptime` and send the output
* `-C CALLBACK` - a local callback command that gets called as a subprocess with each newly received pingout

## Unique identifiers and Retention

When an agent receives a pingout from a peer, it can calculate a unique identifier for the peer. Two peers may not necessarily calculate the same unique identifier, but likely would.

If `-r RETAIN_COUNT` is greater than zero, each pingout causes the peer's unique identifier to be calculated, and the agent stores its latest pingout payload as a record against the unique identifier, along with updating the record's timestamp.

Once the max number of retentions is reached, a new unique identifier causes the oldest identifier to be dropped.

## Timestamps

All timestamps are internally recorded in the host's UTC time, with format `YYYY-MM-DD HH:mm:ss.z`, without exception.

## Queries

Reback can be queried via two HTTP endpoints. Any agent can choose which port to listen on, which can be discovered via a UDP query to the main pinging port.

### `%http-port` to ping receipt port

A UDP packet with a single payload `%http-port` causes the agent to respond with an ASCII-encoded port number to which HTTP queries can be made

### `GET /peers` to HTTP port

Causes the peer to send back a `text/json` list of last seen unique identifiers and their last payloads, as per the retention.

### `GET /info` to HTTP port

Causes the peer to send `text/plain` information back as a response.

It is the peer's discretion to determine what to send back, specified by its `-I INFO_SCRIPT` parameter. By default, this is simply the output of the `uptime; free -h; df -h` shell commands on Nix hosts. Windows hosts it's the output of `powershell -nologo -noprofile Get-Counter`

If the agent should be configured to not send anything, simply use an empty script file. The agent will still send a message stating `All information is private.` as a fixed string.
