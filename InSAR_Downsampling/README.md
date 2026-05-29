# InSAR / Offset Downsampling Cases

This directory collects ECAT examples that convert dense SAR, pixel-offset, and custom raster products into CSI-style downsampled inputs:

```text
<outputName>_ifg.txt
<outputName>_ifg.rsp
<outputName>_ifg.cov
```

Use this page as the case map. The complete field reference stays in the ECAT docs:

- [InSAR downsampling workflow](https://github.com/kefuhe/ECAT/blob/main/docs/workflows/02_insar_downsampling.md)
- [Two-step covariance/downsampling workflow](https://github.com/kefuhe/ECAT/blob/main/docs/workflows/02a_insar_downsampling_two_step.md)
- [Adapter downsampling workflow](https://github.com/kefuhe/ECAT/blob/main/docs/workflows/02b_adapter_downsampling.md)
- [SAR reader reference](https://github.com/kefuhe/ECAT/blob/main/docs/reference/sar_reader.md)
- [Downsampling app reference](https://github.com/kefuhe/ECAT/blob/main/docs/reference/downsampling_app.md)

## Choose A Case

| Data product | Start here | ECAT reader / mode | Main point |
| --- | --- | --- | --- |
| GAMMA binary unwrapped phase | [GAMMA/2022_Menyuan/T128A/std_downsample_superapp](./GAMMA/2022_Menyuan/T128A/std_downsample_superapp/) | `reader: gamma`, `mode: unwrapped_phase` | Standard `-s/-c/-d` workflow for GAMMA `.phs/.azi/.inc/.rsc` products |
| Legacy GAMMA Step1/Step2 scripts | [GAMMA/2022_Menyuan](./GAMMA/2022_Menyuan/) | Compare scripts with current YAML | Historical script structure and its mapping to `ecat-downsample` |
| GeoTIFF value + angle rasters | [GeoTiff/Wushi/insar/std_superapp](./GeoTiff/Wushi/insar/std_superapp/) | `reader: gamma_tiff`, `mode: unwrapped_phase` | GeoTIFF value raster with azimuth/incidence geometry grids |
| GMTSAR LOS / phase products | [GMTSAR/Myanmar](./GMTSAR/Myanmar/) | `reader: gmtsar`, `mode: los_displacement` or `phase_los` | Direct ENU projection grids instead of azimuth/incidence rasters |
| GMTSAR range offset | [GMTSAR/Myanmar](./GMTSAR/Myanmar/) | `reader: gmtsar`, `mode: range_offset` | Value and projection grids share the range/LOS target direction |
| GMTSAR azimuth offset | [GMTSAR/Myanmar](./GMTSAR/Myanmar/) | `reader: gmtsar`, `mode: azimuth_offset` | Along-heading projection; `projection.up` can be omitted for direct azimuth inputs |
| Custom loader or time-series grid reuse | [GAMMA/2022_Menyuan/T128A/std_adapter_downsampling_workflow](./GAMMA/2022_Menyuan/T128A/std_adapter_downsampling_workflow/) | `input_adapter.enabled: true` | Replace only the data-loading layer, then reuse ECAT covariance, quadtree, reports, and optional reference-grid logic |

## Standard Run Order

For a normal SAR/offset product, create or edit `downsample.yml`, then run:

```bash
ecat-downsample -f downsample.yml -s
ecat-downsample -f downsample.yml -c
ecat-downsample -f downsample.yml -d
```

The three flags are stages of one workflow:

| Stage | Purpose | Main outputs |
| --- | --- | --- |
| `-s` | Read the raw product and check units, sign, projection, and quick-look range | `sar_output.txt`, raw figure |
| `-c` | Estimate CSI covariance on background pixels after `covar.mask_out` | `Covariance_estimator.cov`, or East/North estimator files for optical offsets |
| `-d` | Build the downsampling cells and write CSI varres files | `<outputName>_ifg.txt/.rsp/.cov`, decimated check figure, metadata, report |

Run `-s` first whenever the data source, unit scaling, sign convention, projection origin, or reader mode changes.

## Current YAML Semantics

Use the current ECAT field names in new cases:

```yaml
downsample:
  method: std
  std_config:
    min_valid_fraction: 0.1
    split_std_threshold: 0.02
    split_metric_smoothing:
```

Do not copy old script names such as `tolerance`, `std_threshold`, or `smooth` into new YAML files. Current ECAT validates the schema strictly and reports the renamed fields.

For range and azimuth offset cases, prefer a base output name:

```yaml
sar_config:
  outName: S1_T033D
  mode: range_offset
  output_suffix: auto
```

This writes `S1_T033D_RngOff_ifg.txt/.rsp/.cov`. For `azimuth_offset`, the automatic suffix is `_AziOff`. If older generated outputs contain duplicated suffixes such as `_RngOff_RngOff` or `_AziOff_AziOff`, treat them as legacy names and do not copy that pattern into new cases.

## `.rsp` Geometry

Current ECAT rectangular outputs use 18-column full-corner `.rsp` files so that plotting and `from_rsp` reuse preserve the four true lon/lat corners of each cell. Older 10-column rectangular `.rsp` files and 8-column triangular `.rsp` files remain readable:

```yaml
downsample:
  method: from_rsp
  from_rsp_config:
    rsp_file: reference_ifg.rsp
    geometry: auto
```

Use `from_rsp` when several datasets or time steps must share exactly the same sampling cells.

## Keep With Each Case
