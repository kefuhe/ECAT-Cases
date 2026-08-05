 ![Visitors](https://visitor-badge.laobi.icu/badge?page_id=kefuhe.ECAT-Cases) ![GitHub Stars](https://img.shields.io/github/stars/kefuhe/ECAT-Cases?style=social) ![GitHub Forks](https://img.shields.io/github/forks/kefuhe/ECAT-Cases?style=social)
 ![Repository Size](https://img.shields.io/github/repo-size/kefuhe/ECAT-Cases) ![GitHub Language](https://img.shields.io/github/languages/top/kefuhe/ECAT-Cases) ![GitHub Last Commit](https://img.shields.io/github/last-commit/kefuhe/ECAT-Cases)

# ECAT Cases

This repository contains research cases, data-preparation workflows, and advanced examples for the ECAT (Earthquake Cycle Analysis Toolkit).

> ### Data Preparation & Downsampling Examples
>
> | Topic | Example | Data / Reader | What to Learn | Local Directory |
> |-------|---------|---------------|---------------|-----------------|
> | InSAR / offset downsampling overview | InSAR Downsampling | GAMMA, GeoTIFF, GMTSAR direct-projection, adapter | Choose the right reader/mode and convert dense SAR/offset rasters to CSI-style `.txt/.rsp/.cov` inputs | [Details](./InSAR_Downsampling/) |
> | GAMMA binary products | 2022 Menyuan | `reader: gamma`; `unwrapped_phase`, `range_offset`, `azimuth_offset` | GAMMA `.phs/.azi/.inc/.rsc`, old Step1/Step2 scripts, and the newer `ecat-downsample` workflow | [Details](./InSAR_Downsampling/GAMMA/2022_Menyuan/) |
> | GeoTIFF products | Wushi / Chile | `reader: gamma_tiff` or custom input when needed | GeoTIFF value rasters with azimuth/incidence geometry, unit scaling, and standard downsampling outputs | [Details](./InSAR_Downsampling/GeoTiff/) |
> | GMTSAR direct-projection products | Myanmar 2025 / California | `reader: gmtsar`; `los_displacement`, `range_offset`, `azimuth_offset` | GRD/NetCDF value grids plus ENU projection grids for LOS and pixel-offset tracking products | [Details](./InSAR_Downsampling/GMTSAR/) |
> | Adapter and time-series reuse | Menyuan T128A adapter workflow | `input_adapter.enabled: true` | Replace only the data-loading layer while reusing ECAT covariance, quadtree, reporting, and optional reference-grid logic | [Details](./InSAR_Downsampling/GAMMA/2022_Menyuan/T128A/std_adapter_downsampling_workflow/) |
>
> For range/azimuth offset YAMLs, prefer a base `outName` such as `S1_T033D`; `output_suffix: auto` adds `_RngOff` or `_AziOff` and current ECAT avoids duplicating an existing suffix.
>
> Current rectangular ECAT outputs write 18-column full-corner `.rsp` files. Legacy 10-column rectangle `.rsp` files and 8-column triangle `.rsp` files remain readable through `method: from_rsp`.
>
> For the maintained user guide, see the ECAT documentation pages for [InSAR downsampling](https://github.com/kefuhe/ECAT/blob/main/docs/workflows/02_insar_downsampling.md), [adapter downsampling](https://github.com/kefuhe/ECAT/blob/main/docs/workflows/02b_adapter_downsampling.md), and [SAR readers](https://github.com/kefuhe/ECAT/blob/main/docs/reference/sar_reader.md).

> ### Method & Inversion Examples
>
> | 🏷️ Category         | ⚡ Earthquake Example         | 📝 Description (Date, Magnitude, Type)           | 📁 Local Directory                                   |
> |---------------------|------------------------------|--------------------------------------------------|-----------------------------------------------------|
> | Nonlinear Inversion (Single-seg) | [Hotan Earthquake](https://earthquake.usgs.gov/earthquakes/eventpage/us7000abmk/executive)           | 2020-06-25, Mw6.3, Normal                         | [Details](./Cases/Hotan_20200625M6_3/)              |
> |                     | [Iran Earthquake](https://earthquake.usgs.gov/earthquakes/eventpage/us10008ei0/executive)            | 2017-04-05, Mw6.1, Reverse                        | [Details](./Cases/Iran_20170405M6_1/)               |
> |                     | [Taiwan Earthquake](https://earthquake.usgs.gov/earthquakes/eventpage/us7000m9g4/executive)          | 2024-04-05, Mw7.4, Reverse                        | [Details](./Cases/Taiwan_20240405Mw7_4/)            |
> |                     | [Wushi Earthquake](https://earthquake.usgs.gov/earthquakes/eventpage/us7000lsze/executive)           | 2024-01-22, Mw7.0, Strike-slip                    | [Details](./Cases/Wushi_20240122M7_0/)              |
> |                     | [Western Xizang Earthquake](https://earthquake.usgs.gov/earthquakes/eventpage/us6000b26j/executive)  | 2020-07-22, Mw6.3, Normal                         | [Details](./Cases/Western_Xizang_20200722M6_3/)     |
> | Nonlinear Inversion (Multi-segs) | [Ridgecrest Earthquake Sequence](https://earthquake.usgs.gov/earthquakes/eventpage/ci38457511/executive)  | 2019-07-06, Mw7.1, Strike-slip                         | [Details](./Cases/Ridgecrest_20190706Mw7_1/)     |
> | BLSE Linear Inversion | [Dingri Earthquake  2020](https://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form?itype=ymd&yr=2020&mo=3&day=18&otype=ymd&oyr=2020&omo=3&oday=21&jyr=1976&jday=1&ojyr=1976&ojday=1&nday=1&lmw=5&umw=10&lms=0&ums=10&lmb=0&umb=10&llat=28&ulat=29&llon=87&ulon=88&lhd=0&uhd=20&lts=-9999&uts=9999&lpe1=0&upe1=90&lpe2=0&upe2=90&list=5)                                                                            | 2020-03-20, Mw5.7, Normal                         | [Details](./Cases/Dingri_Events/Dingri_20200320Mw5_6/LinearInv/)     |

> ### Real Earthquake Cases
>
> | 🌏 Case Name                                                                 | 📝 Description (Date, Magnitude, Type)        | 📁 Local Directory                                   | 🔗 Zenodo DOI                                      | 📄 Paper DOI |
> |-----------------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------------|----------------------------------------------------|--------------------|
> | Dingri Earthquake 2015                                                      | 2015-04-25, Mw5.7, Normal                    | [Details](./Cases/Dingri_Events/Dingri_20150425Mw5_7/) | [Zenodo](https://doi.org/10.5281/zenodo.13730101)  | [He et al., 2026, CEE](https://doi.org/10.1038/s43247-026-03267-8) |
> | Dingri Earthquake 2020                                                      | 2020-03-20, Mw5.6, Normal                    | [Details](./Cases/Dingri_Events/Dingri_20200320Mw5_6/) | [Zenodo](https://doi.org/10.5281/zenodo.13730101)  | [He et al., 2026, CEE](https://doi.org/10.1038/s43247-026-03267-8) |
> | [Dingri Earthquake 2025](https://earthquake.usgs.gov/earthquakes/eventpage/us6000pi9w/executive) | 2025-01-07, Mw7.0, Normal                    | [Details](./Cases/Dingri_Events/Dingri_20250107Mw7_0/) | [Zenodo](https://doi.org/10.5281/zenodo.13730101)  | [He et al., 2026, CEE](https://doi.org/10.1038/s43247-026-03267-8) |
> | [Sagaing Earthquake 2025](https://earthquake.usgs.gov/earthquakes/eventpage/us7000pn9s/executive) | 2025-03-28, Mw7.8, Strike-slip               | [Details](./Cases/Sagaing_20250328Mw7_8/)              | [Zenodo](https://doi.org/10.5281/zenodo.15460702)  | TBD |

## Usage

Clone this repository to access the cases:

```bash
git clone https://github.com/kefuhe/ECAT-cases.git
```
