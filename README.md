# Report-Back (`reback`)

A simple agent/server that allows individual agents to report back to a server component with basic metrics and information.

## Motivation

I've been in several spaces where keeping track of ad-hoc machines has been necessary. They change IPs, or people set static IPs without consulting, causing various issues.

Installing and setting up a full monitoring solution has not always been possibile. Sometimes the monitoring server itself has needed to be on a potentially transient IP.

This project aims to provide a lightweight solution to this type of issue.

## Design

Reback acts both as server and agent. Each agent broadcasts a single UDP packet periodically containing its hostname and currrent load, and optionally a tag string, with a pingout identifier (application layer information), from which other agents derive the IP and MAC. On receiving a pingout from any other agent, a receiving agent simply records the information to stdout.

```sh
reback [-p PORT] [-T TAGS] [-A] [-P PERIODICITY] BROADCAST_IP
```

* `BROADCAST_IP` - the broadcast IP to send pingouts to
* `-p PORT` - the port to listen and broadcast on. All agents should use the same port
    * default `42324`
* `-T TAGS` - an agent can specify tags, in which case it will only record pingouts that carry at least one tag in common
    * default empty - agent sends no tags, and records all
* `-A` - record all, even if tags were specififed
* `-P PERIODICITY` - how frequently to send a pingout, in seconds
    * default 30
    * if `prime` is specified, uses a random choice from `17, 19, 23, 29, 31, 37, 41` (to be checked) (prime numbers)
    * if `random` is specified, chooses a new prime number after each pingout
