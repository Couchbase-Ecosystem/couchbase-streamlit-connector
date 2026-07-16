from importlib.metadata import version

try:
    from reo_census import ReoEventLogger

    _pkg_version = version("couchbase-streamlit-connector")
    _logger = ReoEventLogger(
        endpoint_url="https://telemetry.reo.dev/data",
        timeout=3.0,
        package_name="couchbase-streamlit-connector",
        package_version=_pkg_version,
    )
    _logger.log_event()
except Exception:
    pass
