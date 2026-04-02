# Grafana Billing Metrics Reference

This document defines the key metrics used for observability billing and how they're calculated.

## Prometheus Metrics

### Active Time Series

**Metric**: `prometheus_tsdb_head_series`

The number of unique time series currently in Prometheus's head block (recent data in memory).

- **Billing Impact**: Primary billing dimension for Grafana Cloud Metrics
- **Calculation**: 95th percentile over billing period (forgives ~36 hours of spikes per month)
- **Optimization**: Reduce label cardinality, drop unused metrics

### Data Points Per Minute (DPM)

**Metric**: `rate(prometheus_tsdb_head_samples_appended_total[5m]) * 60`

The rate at which new data points are being ingested.

- **Billing Impact**: Secondary billing dimension
- **Calculation**: DPM = samples/second × 60
- **Optimization**: Increase scrape interval, reduce metric count

### Head Chunks

**Metric**: `prometheus_tsdb_head_chunks`

Number of chunks in the head block. Each time series has multiple chunks.

- **Billing Impact**: Memory usage indicator
- **Normal Ratio**: ~2-3 chunks per active series

### TSDB Storage

**Metric**: `prometheus_tsdb_storage_blocks_bytes`

Total on-disk storage used by all TSDB blocks.

- **Billing Impact**: Storage costs
- **Factors**: Retention period, series count, sample rate

### Cardinality Analysis

**Endpoint**: `/api/v1/status/tsdb`

Returns breakdown of series count by:
- `seriesCountByMetricName` - Which metrics have most series
- `labelValueCountByLabelName` - Which labels have most unique values
- `memoryInBytesByLabelName` - Memory cost per label

## Loki Metrics

### Bytes Received

**Metric**: `loki_distributor_bytes_received_total`

Cumulative bytes ingested by Loki distributors.

- **Billing Impact**: Primary billing dimension (GB ingested)
- **Labels**: `tenant` for multi-tenant deployments

### Ingestion Rate

**Calculation**: `rate(loki_distributor_bytes_received_total[5m])`

Current ingestion rate in bytes/second.

- **Conversion**: GB/day = bytes/sec × 86400 / (1024³)
- **Billing**: Grafana Cloud charges per GB ingested

### Active Streams

**Metric**: `loki_ingester_memory_streams`

Number of active log streams (unique label combinations).

- **Billing Impact**: Affects query performance, not direct billing
- **Optimization**: Reduce unique label values

### Memory Chunks

**Metric**: `loki_ingester_memory_chunks`

Chunks held in memory by ingesters.

- **Billing Impact**: Memory usage, not direct billing
- **Optimization**: Tune `chunk_idle_period`, `chunk_target_size`

### Rejected Bytes

**Metric**: `loki_distributor_bytes_received_total{reason=~".+"}`

Bytes rejected due to rate limiting or validation errors.

- **Billing Impact**: Not billed, but indicates problems
- **Common Reasons**: Rate limiting, line too long, stream limit

## Grafana Cloud Billing Model

### Metrics (Prometheus)

| Dimension | Unit | Notes |
|-----------|------|-------|
| Active Series | per 1K series | 95th percentile |
| DPM | per 1K DPM | 95th percentile |

### Logs (Loki)

| Dimension | Unit | Notes |
|-----------|------|-------|
| GB Ingested | per GB | Primary charge |
| GB Queried | per GB | Fair use: 100× ingested free |

## Cost Optimization Strategies

### Prometheus

1. **Reduce cardinality**: Remove high-cardinality labels (UUIDs, timestamps)
2. **Drop unused metrics**: Use relabeling to filter at scrape time
3. **Increase scrape interval**: 30s → 60s halves DPM
4. **Recording rules**: Pre-aggregate expensive queries

### Loki

1. **Drop debug logs**: Filter verbose logs before ingestion
2. **Compress logs**: Use structured logging with templates
3. **Reduce label cardinality**: Static labels only
4. **Use Adaptive Logs**: Automatically identify droppable patterns

## References

- [Grafana Cloud Pricing](https://grafana.com/pricing/)
- [Analyze Metrics Usage](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/analyze-costs/metrics-costs/)
- [Reduce Logs Costs](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/logs-costs/)
- [Prometheus TSDB](https://prometheus.io/docs/prometheus/latest/storage/)
