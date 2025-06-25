** CURRENTLY TESTING - USE WITH CAUTION **

[![Build and publish the container image](https://github.com/sgofferj/tak-feeder-weather-fmi/actions/workflows/actions.yml/badge.svg)](https://github.com/sgofferj/tak-feeder-weather-fmi/actions/workflows/actions.yml)

# tak-feeder-weather-fmi
Get latest weather observation data from the Finnish Meteorological Institute and feed them to a TAK server

(C) 2025 Stefan Gofferje

Licensed under the GNU General Public License V3 or later.

## Description
The Finnish Traffic Authority provides free API access to the AIS data from their receiver network
which covers most of the Baltic Sea, the Gulf of Finland and inland waters. This container connects
to the Digitraffic MQTT server and feeds the data to a TAK server. The position data is submitted
separately from the metadata (ship's name, etc.), so after starting the container, it will take
some time before all ships are identified and show their proper icons and data.

## Configuration
The following values are supported and can be provided either as environment variables or through an .env-file.

| Variable | Default | Purpose |
|----------|---------|---------|
| COT_URL | empty | (mandatory) TAK server full URL, e.g. ssl://takserver:8089 |
| PYTAK_TLS_CLIENT_CERT | empty | (mandatory for ssl) User certificate in PEM format |
| PYTAK_TLS_CLIENT_KEY | empty | (mandatory for ssl) User certificate key file (xxx.key) |
| PYTAK_TLS_DONT_VERIFY | 1 | (optional) Verify the server certificate (0) or not (1) |
| TAK_PROTO | 0 | (optional) Choose the protocol (see [PyTAK docs](https://pytak.readthedocs.io/en/stable/configuration/)) |

## Certificates
These are the server-issued certificate and key files. Before using, the password needs to be removed from the key file with `openssl rsa -in cert.key -out cert-nopw.key`. OpenSSL will ask for the key password which usually is "atakatak".

## Container use
First, get your certificate and key and copy them to a suitable folder which needs to be added as a volume to the container.

### Image
The image is built for AMD64 and ARM64 and pushed to ghcr.io: *ghcr.io/sgofferj/tak-feeder-weather-fmi:latest*

### Docker compose
Here is an example for a docker-compose.yml file:
```
version: '2.0'

services:
  weather-fmi:
    image: ghcr.io/sgofferj/tak-feeder-weather-fmi:latest
    restart: always
    networks:
      - default
    volumes:
      - <path to data-directory>:/data:ro
    environment:
      - COT_URL=ssl://tak-server:8089
      - PYTAK_TLS_CLIENT_CERT=/data/cert.pem
      - PYTAK_TLS_CLIENT_KEY=/data/key.pem
      - PYTAK_TLS_DONT_VERIFY=1
      - TAK_PROTO=0

networks:
  default:
