"""Database migrations for cryptocurrency data"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


def upgrade():
    """Insert top 10 cryptocurrencies"""
    cryptocurrencies_table = sa.table(
        'cryptocurrencies',
        sa.column('symbol', sa.String),
        sa.column('name', sa.String),
        sa.column('current_price', sa.Float),
        sa.column('market_cap', sa.Float),
        sa.column('volume_24h', sa.Float),
        sa.column('updated_at', sa.DateTime),
    )
    
    top_cryptos = [
        {
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'ETH',
            'name': 'Ethereum',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'USDT',
            'name': 'Tether',
            'current_price': 1.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'BNB',
            'name': 'Binance Coin',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'USDC',
            'name': 'USD Coin',
            'current_price': 1.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'XRP',
            'name': 'Ripple',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'SOL',
            'name': 'Solana',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'TRX',
            'name': 'TRON',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'HYPE',
            'name': 'Hyperliquid',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
        {
            'symbol': 'DOGE',
            'name': 'Dogecoin',
            'current_price': 0.0,
            'market_cap': 0.0,
            'volume_24h': 0.0,
        },
    ]
    
    for crypto in top_cryptos:
        op.execute(
            cryptocurrencies_table.insert().values(
                symbol=crypto['symbol'],
                name=crypto['name'],
                current_price=crypto['current_price'],
                market_cap=crypto['market_cap'],
                volume_24h=crypto['volume_24h'],
                updated_at=datetime.utcnow(),
            )
        )


def downgrade():
    """Remove seed data"""
    op.execute("DELETE FROM cryptocurrencies WHERE symbol IN ('BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'SOL', 'TRX', 'HYPE', 'DOGE')")
