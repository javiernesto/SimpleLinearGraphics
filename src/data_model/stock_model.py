import pandas as pd
import base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from stock import Stock
from price import Price

class StockModel(object):
    _db_config = ''
    engine = object

    def __init__(self, db_config):
        self._db_config = db_config
        self.engine = create_engine(self._db_config)
        with self.engine.begin() as conn:
            base.Base.metadata.create_all(conn)

    """
    Price Table
    """

    def get_symbol_prices(self, symbol, start_date, end_date):
        Session = sessionmaker(bind=self.engine, future=True)
        session = Session()
        try:
            query = session.execute(
                select(
                    Price.day,
                    Price.symbol,
                    Price.open,
                    Price.close,
                    Price.high,
                    Price.low
                ).where(
                    Price.symbol == symbol,
                    Price.day >= start_date,
                    Price.day <= end_date
                )
            ).all()
            # Getting the column names returned by the query
            query_columns = query[0].keys() if query else []

            # Creating a dictionary of the data returned by the query
            data = [dict(zip(query_columns, row)) for row in query]

            # Saving the query data in a dataframe
            df = pd.DataFrame(data)

            return df
        except Exception as ex:
            print(ex.args)
            return pd.DataFrame()