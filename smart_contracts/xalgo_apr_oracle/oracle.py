from beaker import *
from pyteal import *

class APROracleState:
    # Current APR value stored as basis points (1% = 100)
    current_apr = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Current APR in basis points"
    )
    
    # Timestamp of last update
    last_update = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Timestamp of last update"
    )
    
    # Address authorized to update the oracle
    auth_address = GlobalStateValue(
        stack_type=TealType.bytes,
        descr="Authorized updater address"
    )

class APROracle(Application):
    def __init__(self):
        super().__init__()
        self.state = APROracleState()

    @create
    def create(self):
        """Initialize the oracle contract"""
        return Seq([
            self.state.auth_address.set(Global.creator_address()),
            self.initialize_application_state()
        ])

    @external
    def update_apr(self, apr: abi.Uint64, *, output: abi.Uint64):
        """Update the APR value (restricted to authorized address)"""
        return Seq([
            Assert(Txn.sender() == self.state.auth_address.get()),
            Assert(apr.get() <= Int(10000)), # Max 100% APR (10000 basis points)
            self.state.current_apr.set(apr.get()),
            self.state.last_update.set(Global.latest_timestamp()),
            output.set(apr.get())
        ])

    @external(read_only=True)
    def get_apr(self, *, output: abi.Uint64):
        """Get the current APR value"""
        return output.set(self.state.current_apr.get())

    @external(read_only=True)
    def get_last_update(self, *, output: abi.Uint64):
        """Get timestamp of last update"""
        return output.set(self.state.last_update.get())
