# My Package

This is the SDK package for actxa-insights clients.

## Create new version
```
in setup.py file, create new version
rename folder dist to dist_v.[previous version] (contain previous version)
```

## Build package

```
python -m pip install --upgrade build twine
python -m build
twine upload dist/*
```

## Installation

```
pip install actxa-insights
```

## Usage

```python
from actxa_insights import predict_bgm_range_app

response = predict_bgm_range_app(
    "dev",
    "186d1e95-4fbe-4f74-802d-8a52b4637aaa",
    "ec4a2e2a-51e9-4d9c-8ae6-b058a6975154",
    "serial-number",
    10015678,
    {
        "start": "2024-09-12 09:53:22",
        "end": "2024-09-12 09:58:33",
        "fasting": True,
        "within2HrsMeal": False,
        "nBit": 23,
        "ppgData": [
            {
                "ppg": [
                    5956031,
                    5949472,
                    5942943,
                    5938014,
                    5934479,
                    5931011,
                    5926540,
                    5923345,
                    5927220,
                    5932507,
                    5939766,
                    5941773,
                    5937539,
                    5931266,
                    5930365,
                    5934972,
                    5939528,
                    5942112,
                    5942775,
                    5942079,
                    5941772,
                    5943387,
                    5946278,
                    5948828,
                    5950833,
                    5952108,
                    5953774,
                    5955423,
                    5956630,
                    5955560,
                    5952499,
                    5948385,
                    5943319,
                    5938611,
                    5934377,
                    5931351,
                    5930841,
                    5932269,
                    5933340,
                    5934956,
                    5934820,
                    5933561,
                    5933664,
                    5935126,
                    5936672,
                    5937250,
                    5936315,
                    5935839,
                    5936298,
                    5937964,
                ],
                "timestamp": "01:44:46",
            },
            {
                "ppg": [
                    5956036,
                    5949473,
                    5942946,
                    5938016,
                    5934479,
                    5931011,
                    5926540,
                    5923345,
                    5927220,
                    5932507,
                    5939766,
                    5941773,
                    5937539,
                    5931266,
                    5930365,
                    5934972,
                    5939528,
                    5942112,
                    5942775,
                    5942079,
                    5941772,
                    5943387,
                    5946278,
                    5948828,
                    5950833,
                    5952108,
                    5953774,
                    5955423,
                    5956630,
                    5955560,
                    5952499,
                    5948385,
                    5943319,
                    5938611,
                    5934377,
                    5931351,
                    5930841,
                    5932269,
                    5933340,
                    5934956,
                    5934820,
                    5933561,
                    5933664,
                    5935126,
                    5936672,
                    5937250,
                    5936315,
                    5935839,
                    5936298,
                    5937964,
                ],
                "timestamp": "01:44:46",
            },
        ],
    },
)
print(response)

```