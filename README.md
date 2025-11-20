# Report-Back (`reback`)

A simple agent/server that allows individual agents to report back to a server component with basic metrics and information.

## Motivation

I've been in several spaces where keeping track of ad-hoc machines has been necessary. They change IPs, or people set static IPs without consulting, causing various issues.

Installing and setting up a full monitoring solution has not always been possibile. Sometimes the monitoring server itself has needed to be on a potentially transient IP.

This project aims to provide a lightweight solution to this type of issue.

## Design

Reback acts both as server and agent. Each agent broadcasts a single UDP packet periodically containing its hostname and currrent load, and optionally a tag string, with a pingout identifier (application layer information), from which other agents derive the IP and MAC. On receiving a pingout from any other agent, a receiving agent simply records the information to stdout.

```sh
reback up [-p PORT] [-T TAGS] [-A] [-P PERIODICITY] [-r RETAIN_COUNT] [-I INFO_SCRIPT] BROADCAST_IP
```

* `BROADCAST_IP` - the broadcast IP to send pingouts to
* `-p PORT` - the port to listen and broadcast on. All agents should use the same port
    * default `42324`
* `-T TAGS` - an agent can specify tags, in which case it will only record pingouts that carry at least one tag in common
    * default empty - agent sends no tags, and records all
* `-A` - record all, even if tags were specififed
    * default `false`
* `-P PERIODICITY` - how frequently to send a pingout, in seconds
    * default `30`
    * if `prime` is specified, uses a random choice from `17, 19, 23, 29, 31, 37, 41` (to be checked) (prime numbers)
    * if `random` is specified, chooses a new prime number after each pingout
* `-r RETAIN_COUNT` - retain last entry for `RETAIN_COUNT` number of peers
    * default `20`
* `-I INFO_SCRIPT` - path to a script to run when queried for information
    * default is to run `uptime` and send the output

## Unique identifiers

When an agent receives a pingout from a peer, it can calculate a unique identifier for the peer. Two peers may not necessarily calculate the same unique identifier, but likely would.

If `-r RETAIN_COUNT` is greater than zero, each pingout causes the peer's unique identifier to be calculated, and the agent stores its latest pingout payload as a record against the unique identifier.

Once the max number of retentions is reached, a new unique identifier causes the oldest identifier to be dropped.

## Queries

Reback can be used to query a peer - a simple HTTP GET request to `/peers` causes the peer to send back a JSON encoded list of last seen unique identifiers and their last payloads, as per the retention.

```sh
reback peers IP:PORT
```

Reback can also request information from a peer via a HTTP GET request to `/info`. It is the peer's discretion to determine what to send back, specified by its `-I INFO_SCRIPT` parameter. By default, this is simply the output of the `uptime; free -h; df -h` shell commands on Nix hosts. Windows hosts it's the output of `powershell -nologo -noprofile Get-Counter`

```sh
reback info IP:PORT
```

If the agent should be configured to not send anything, simply use an empty script file. The agent will still send a message stating `All information is private.` as a fixed string.
