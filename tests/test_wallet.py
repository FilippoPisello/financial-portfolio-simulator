from financial_portfolio_simulator.wallet import StockPosition


class TestStock:
    def sample_stock(self):
        return StockPosition(investment=100, units=10)

    def test_if_buy_units_then_investment_and_units_change(self):
        mystock = self.sample_stock()
        mystock.buy_units(units=5, market_price=5)
        assert mystock.investment == 125
        assert mystock.units == 15

    def test_if_buy_value_then_investment_and_units_change(self):
        mystock = self.sample_stock()
        mystock.buy_value(value=100, market_price=5)
        assert mystock.investment == 200
        assert mystock.units == 30

    def test_holding_price_is_average_unit_price(self):
        mystock = self.sample_stock()
        assert mystock.holding_price == 100 / 10

    def test_countervalue_is_market_price_times_number_of_units(self):
        mystock = self.sample_stock()
        assert mystock.countervalue(market_price=5) == 10 * 5

    def test_return_on_investment_is_ratio_of_holding_price_to_market_price(self):
        mystock = self.sample_stock()
        assert mystock.return_on_investment(market_price=20) == (20 / (100 / 10) - 1)
