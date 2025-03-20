from aiohttp import ClientSession
from datetime import datetime
from logging import exception
from prometheus_client import start_http_server, Enum, Gauge
from shellrecharge import Api, LocationEmptyError, LocationValidationError
from time import sleep

metrics = {
    "address": Gauge(
        "cic_address",
        "Address information",
        ["station_id", "address", "street", "postal_code", "city", "country"],
    ),
    "connector_power": Gauge(
        "cic_connector_power",
        "Connector max electric power",
        ["station_id", "address", "evse_id", "connector_id"],
    ),
    "evse_status": Enum(
        "cic_evse_status",
        "Status of evse",
        ["station_id", "address", "evse_id"],
        states=["Available", "Unavailable", "Occupied", "Unknown"],
    ),
    "evse_updated": Gauge(
        "cic_evse_updated",
        "Evse last updated time",
        ["station_id", "address", "evse_id"],
    ),
    "operator_name": Gauge(
        "cic_operator_name", "Operator name", ["station_id", "address", "operator_name"]
    ),
    "station_exists": Gauge("cic_station_exists", "Station Exists", ["station_id"]),
}


def iso_to_epoch(iso_string):
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp()


def set_metrics(station, found):
    if not found:
        metrics["station_exists"].labels(station_id=station).set(0)
        return
    address = f"{station.address.streetAndNumber}, {station.address.postalCode} {station.address.city}"
    metrics["address"].labels(
        station_id=station.externalId,
        address=address,
        street=station.address.streetAndNumber,
        postal_code=station.address.postalCode,
        city=station.address.city,
        country=station.address.country,
    ).set(1)
    metrics["operator_name"].labels(
        station_id=station.externalId,
        address=address,
        operator_name=station.operatorName,
    ).set(1)
    metrics["station_exists"].labels(station_id=station.externalId).set(1)
    for evse in station.evses:
        metrics["evse_status"].labels(
            station_id=station.externalId, address=address, evse_id=evse.externalId
        ).state(evse.status)
        metrics["evse_updated"].labels(
            station_id=station.externalId, address=address, evse_id=evse.externalId
        ).set(iso_to_epoch(evse.updated))
        for connector in evse.connectors:
            metrics["connector_power"].labels(
                station_id=station.externalId,
                address=address,
                evse_id=evse.externalId,
                connector_id=connector.externalId,
            ).set(connector.electricalProperties.maxElectricPower)


async def run_metrics_loop(stations, interval):
    async with ClientSession() as session:
        api = Api(session)
        while True:
            for station_id in stations:
                try:
                    station = await api.location_by_id(station_id)
                    set_metrics(station, True)
                except (LocationEmptyError, LocationValidationError):
                    set_metrics(station_id, False)
                except (CancelledError, ClientError, TimeoutError) as err:
                    logging(
                        f"An exception occured while connecting with the API: {err}"
                    )
            sleep(interval)
