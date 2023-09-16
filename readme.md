# financial-portfolio-simulator

Once completed, this tool should allow users to test how one or more investment strategies would have performed against a stock using historical data.

## Scoping

The key idea is that the tool will create _n_ simulations for each of the strategies provided, changing the starting - and thus ending - date of a fixed-length simulation. Finally, the distribution of returns for each strategy is compared.

### Requirements

#### Inputs

- Settings are provided through a `config` file
- The following parameters can be specified:
  - `strategies`: list of dict where the key is the name of the strategy and the value is a dict at its time, whose keys are the names of the strategy-specific settings and the values are the settings values.
  - `ticker`: the ticker on the stock on which to run the simulation on.
  - `min_start_date`: the earliest date data can be pulled from.
  - `max_start_date`: the latest date data can be pulled from.
  - `number_of_financial_periods`: how many financial periods the simulation should last for.
  - `number_of_simulations`: how many simulations for each strategy should be run.

#### Outputs

- An excel file containing the day-by-day aggregate of the simulations:
  - There is one strategy per tab.
  - It contains daily values for the min, -2sd, median, +2sd, max for
    - Invested amount
    - Countervalue
    - ROI
- A chart containing the overlap distributions of the closing ROI per strategy (histograms)
- A two-panels chart showing
  - Invested amount / countervalue per day
  - ROI per day

### Architecture

#### High-level view

- Config is loaded from a `yml` file
- `n` datasets with random - but constrained - starting dates are created according to the config settings
- For each strategy and each dataset the following is computed:
  - Amount invested per period (to be intended as generic day succession _d_, _d+1_, ..., )
  - Countervalue per period
  - ROI per period
  - Closing ROI
- All results are aggregated into the desired output
