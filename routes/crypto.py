from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import Cryptocurrency
from schemas import CryptocurrencyResponse
from services.crypto_service import crypto_service
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/cryptocurrencies",
    tags=["cryptocurrencies"],
)


@router.get("/", response_model=List[CryptocurrencyResponse])
async def get_cryptocurrencies(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get list of cryptocurrencies"""
    cryptos = db.query(Cryptocurrency).offset(skip).limit(limit).all()
    return cryptos


@router.get("/{crypto_id}", response_model=CryptocurrencyResponse)
async def get_cryptocurrency(
    crypto_id: int,
    db: Session = Depends(get_db),
):
    """Get specific cryptocurrency"""
    crypto = db.query(Cryptocurrency).filter(Cryptocurrency.id == crypto_id).first()
    
    if not crypto:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")
    
    return crypto


@router.get("/symbol/{symbol}", response_model=CryptocurrencyResponse)
async def get_cryptocurrency_by_symbol(
    symbol: str,
    db: Session = Depends(get_db),
):
    """Get cryptocurrency by symbol"""
    crypto = db.query(Cryptocurrency).filter(
        Cryptocurrency.symbol == symbol.upper()
    ).first()
    
    if not crypto:
        raise HTTPException(status_code=404, detail=f"Cryptocurrency {symbol} not found")
    
    return crypto


@router.post("/sync/{symbol}")
async def sync_cryptocurrency(
    symbol: str,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    """Sync cryptocurrency data from exchange"""
    try:
        # Get cryptocurrency from database
        crypto = db.query(Cryptocurrency).filter(
            Cryptocurrency.symbol == symbol.upper()
        ).first()
        
        if not crypto:
            raise HTTPException(status_code=404, detail=f"Cryptocurrency {symbol} not found")
        
        # Fetch from exchange
        trading_pair = f"{symbol.upper()}/USDT"
        ticker = crypto_service.get_ticker(trading_pair)
        
        # Update cryptocurrency
        crypto.current_price = ticker.get('last', 0.0)
        crypto.volume_24h = ticker.get('quoteVolume', 0.0)
        
        db.commit()
        
        return {
            "message": f"✅ {symbol.upper()} synced successfully",
            "symbol": symbol.upper(),
            "price": crypto.current_price,
            "volume_24h": crypto.volume_24h,
        }
        
    except Exception as e:
        logger.error(f"Error syncing {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error syncing data: {str(e)}")


@router.post("/sync-all")
async def sync_all_cryptocurrencies(
    db: Session = Depends(get_db),
):
    """Sync all cryptocurrencies from exchange"""
    try:
        cryptos = db.query(Cryptocurrency).all()
        
        if not cryptos:
            raise HTTPException(status_code=404, detail="No cryptocurrencies found in database")
        
        synced = 0
        failed = 0
        
        for crypto in cryptos:
            try:
                trading_pair = f"{crypto.symbol}/USDT"
                ticker = crypto_service.get_ticker(trading_pair)
                
                crypto.current_price = ticker.get('last', 0.0)
                crypto.volume_24h = ticker.get('quoteVolume', 0.0)
                
                synced += 1
            except Exception as e:
                logger.warning(f"Failed to sync {crypto.symbol}: {str(e)}")
                failed += 1
        
        db.commit()
        
        return {
            "message": "Sync completed",
            "synced": synced,
            "failed": failed,
            "total": len(cryptos),
        }
        
    except Exception as e:
        logger.error(f"Error syncing all cryptocurrencies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")