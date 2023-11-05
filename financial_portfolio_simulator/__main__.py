from financial_portfolio_simulator import OUTPUT_DIR
from financial_portfolio_simulator.config import ProjectConfig, load_config
from financial_portfolio_simulator.dataset import (
    StockDataDownloader,
    YahooFinanceDataDownloader,
    generate_randomized_parameters,
)
from financial_portfolio_simulator.plots import make_plot_roi_distribution
from financial_portfolio_simulator.returns import Returns, calculate_returns
from financial_portfolio_simulator.statistics import (
    align_returns_length,
    compute_returns_statistics_over_time,
    save_dataframe_to_excel,
)


def main():
    config = load_config()

    data_downloader = YahooFinanceDataDownloader()

    single_runs_results = run_simulations(config, data_downloader)
    for strategy_label, results in single_runs_results.items():
        aligned_results = align_returns_length(results)
        summary = compute_returns_statistics_over_time(aligned_results)
        save_dataframe_to_excel(summary, OUTPUT_DIR / "summary.xlsx", strategy_label)
        make_plot_roi_distribution(aligned_results)


def run_simulations(
    config: ProjectConfig,
    data_downloader: StockDataDownloader,
) -> dict[str, list[Returns]]:
    results = {strategy_label: [] for strategy_label in config.strategies.keys()}
    for _ in range(config.number_of_simulations):
        parameters = generate_randomized_parameters(
            ticker=config.ticker,
            min_start_date=config.min_start_date,
            max_start_date=config.max_start_date,
            number_of_financial_periods=config.number_of_financial_periods,
        )
        data = data_downloader.download(
            ticker=parameters.ticker,
            start_date=parameters.start_date,
            end_date=parameters.end_date,
        )
        for strategy_label, strategy_settings in config.strategies.items():
            result = calculate_returns(
                data=data,
                strategy_label=strategy_label,
                strategy_settings=strategy_settings,
            )
            results[strategy_label].append(result)
    return results


if __name__ == "__main__":
    main()
