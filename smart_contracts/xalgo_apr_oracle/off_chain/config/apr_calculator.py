rom algosdk import account, mnemonic, transaction
from algosdk.v2client import algod
import json
import time
from datetime import datetime, timedelta

class APRCalculator:
    def __init__(self, algod_client, folks_finance_sdk, oracle_id, auth_key):
        self.algod_client = algod_client
        self.folks_finance_sdk = folks_finance_sdk
        self.oracle_id = oracle_id
        self.auth_key = auth_key

    async def calculate_apr(self):
        """Calculate APR based on xALGO value change"""
        try:
            # Get current consensus state
            current_state = await self.folks_finance_sdk.getConsensusState()
            
            # Store current values
            current_time = int(time.time())
            current_xalgo_value = current_state.xalgoPerAlgo
            
            # Wait for measurement period (e.g., 1 hour)
            await asyncio.sleep(3600)
            
            # Get new consensus state
            new_state = await self.folks_finance_sdk.getConsensusState()
            new_xalgo_value = new_state.xalgoPerAlgo
            
            # Calculate value change
            value_change = (new_xalgo_value - current_xalgo_value) / current_xalgo_value
            
            # Annualize the rate (multiply by number of periods in a year)
            periods_per_year = 365 * 24  # assuming hourly measurements
            apr = value_change * periods_per_year
            
            # Convert to basis points (1% = 100 basis points)
            apr_basis_points = int(apr * 10000)
            
            return apr_basis_points
            
        except Exception as e:
            print(f"Error calculating APR: {e}")
            return None

    async def update_oracle(self, apr_basis_points):
        """Push new APR value to on-chain oracle"""
        try:
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            
            # Create application call transaction
            app_args = [
                "update_apr",
                apr_basis_points.to_bytes(8, 'big')
            ]
            
            txn = transaction.ApplicationCallTxn(
                sender=account.get_address(self.auth_key),
                sp=params,
                index=self.oracle_id,
                on_complete=transaction.OnComplete.NoOpOC,
                app_args=app_args
            )
            
            # Sign and send transaction
            signed_txn = txn.sign(self.auth_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            # Wait for confirmation
            transaction.wait_for_confirmation(self.algod_client, tx_id)
            
            print(f"Successfully updated APR to {apr_basis_points/100}%")
            
        except Exception as e:
            print(f"Error updating oracle: {e}")
