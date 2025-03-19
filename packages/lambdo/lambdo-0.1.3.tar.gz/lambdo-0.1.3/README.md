# Lambdo

Lamb*do* is a CLI tool that utilizes the Lambda GPU Cloud Public APIs

![help_output.png](lambdo/static/help_output.png)

## Lambda Labs Cloud API

https://docs.lambdalabs.com/public-cloud/cloud-api/

## Lambda Labs Redoc

https://cloud.lambdalabs.com/api/v1/docs

## How does it work?

Lambdo was built using [Typer](https://typer.tiangolo.com) by tiangolo

All the features of Typer are included in this package and work out of the box, including command completion. Be sure
to install it!

I utilized the `requests` library to handle the API calls and store project variables in `~/.lambdo/config.json`.

## Documentation

**Usage**:

```console
$ lambdo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `filesystems`: List your persistent storage filesystems
* `firewall`: List your firewall rules
* `images`: List available images
* `instances`: Manage your Lambda GPU Cloud instances
* `instance-types`: List the instances types offered by Lambda...
* `setup`: Setup Lambdo with your API KEY and SSH path
* `ssh-keys`: Manage SSH Keys for your instances

## `lambdo filesystems`

List your persistent storage filesystems

**Usage**:

```console
$ lambdo filesystems [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a filesystem
* `delete`: Delete a filesystem

### `lambdo filesystems create`

Create a filesystem

**Usage**:

```console
$ lambdo filesystems create [OPTIONS]
```

**Options**:

* `--name TEXT`: The name of the filesystem  [required]
* `--region TEXT`: The region name  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

### `lambdo filesystems delete`

Delete a filesystem

**Usage**:

```console
$ lambdo filesystems delete [OPTIONS]
```

**Options**:

* `--id TEXT`: The id of the filesystem you want to delete  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

## `lambdo firewall`

List your firewall rules

**Usage**:

```console
$ lambdo firewall [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

**Commands**:

* `update`: Overwrites the inbound firewall rules...

### `lambdo firewall update`

Overwrites the inbound firewall rules currently active

**Usage**:

```console
$ lambdo firewall update [OPTIONS]
```

**Options**:

* `-p, --protocol TEXT`
* `-r, --port-range TEXT`: Range of ports allowed
* `-s, --source-net TEXT`: Source network allowed
* `--description TEXT`: Description of the firewall rule
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

## `lambdo images`

List available images

**Usage**:

```console
$ lambdo images [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

## `lambdo instances`

Manage your Lambda GPU Cloud instances

**Usage**:

```console
$ lambdo instances [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

**Commands**:

* `detail`: Retrieve the details of an instance
* `create`: Create an instance
* `restart`: Restart instance(s)
* `delete`: Delete instance(s)

### `lambdo instances detail`

Retrieve the details of an instance

**Usage**:

```console
$ lambdo instances detail [OPTIONS]
```

**Options**:

* `--inst-id TEXT`: The id of the instance  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

### `lambdo instances create`

Create an instance

**Usage**:

```console
$ lambdo instances create [OPTIONS]
```

**Options**:

* `--region-name TEXT`: The region name  [required]
* `--instance-type-name TEXT`: The instance type name  [required]
* `--ssh-key-names TEXT`: The name of the ssh key  [required]
* `--filesystems TEXT`: The name of the filesystems  [required]
* `--quantity INTEGER`: The quantity of instances  [default: 1]
* `--name TEXT`: The custom name of the instance
* `--from-file TEXT`: Path to a file containing required parameters
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

### `lambdo instances restart`

Restart instance(s)

**Usage**:

```console
$ lambdo instances restart [OPTIONS]
```

**Options**:

* `--inst-id TEXT`: The id of the instance(s) you want to restart  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

### `lambdo instances delete`

Delete instance(s)

**Usage**:

```console
$ lambdo instances delete [OPTIONS]
```

**Options**:

* `--inst-id TEXT`: The id of the instance(s) you want to delete  [required]
* `--from-file TEXT`: Path to a file containing required parameters
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

## `lambdo instance-types`

List the instances types offered by Lambda GPU Cloud

**Usage**:

```console
$ lambdo instance-types [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--available`: Show only available instance types.
* `--unavailable`: Show only unavailable instance types.
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

**Commands**:

* `gpu`: Search for a particular GPU by name
* `location`: Search for GPUs by location

### `lambdo instance-types gpu`

Search for a particular GPU by name

**Usage**:

```console
$ lambdo instance-types gpu [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Provide the name of the gpu  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

### `lambdo instance-types location`

Search for GPUs by location

**Usage**:

```console
$ lambdo instance-types location [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Search by location  [required]
* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

## `lambdo setup`

Setup Lambdo with your API KEY and SSH path

**Usage**:

```console
$ lambdo setup [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--api-key TEXT`: [required]
* `--ssh-path TEXT`: [required]
* `--help`: Show this message and exit.

## `lambdo ssh-keys`

Manage SSH Keys for your instances

**Usage**:

```console
$ lambdo ssh-keys [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --debug`: Print additional helpful information.
* `--help`: Show this message and exit.

**Commands**:

* `add`: Add an SSH key
* `delete`: Delete an SSH key

### `lambdo ssh-keys add`

Add an SSH key

**Usage**:

```console
$ lambdo ssh-keys add [OPTIONS]
```

**Options**:

* `-n, --new`: Add a new SSH Key
* `--help`: Show this message and exit.

### `lambdo ssh-keys delete`

Delete an SSH key

**Usage**:

```console
$ lambdo ssh-keys delete [OPTIONS]
```

**Options**:

* `--key TEXT`: The id of the SSH key you want to delete  [required]
* `--help`: Show this message and exit.
