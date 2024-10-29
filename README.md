# Algorand Hackathon Challenge - Create an xALGO APR Oracle

## Challenge Overview
Your task is to build an oracle for the APR of the Folks Finance Liquid Staking token xALGO.
**SUBMISSIONS SHOULD BE A DONE WITH A PR ON THIS REPO**

## Background
Folks Finance's xALGO is the primary liquid staking token on the Algorand blockchain. It represents staked ALGO and allows users to earn Algorand Consensus Rewards while remaining liquid on DeFi. By staking ALGO through Folks Finance, users receive xALGO tokens, which accrue value over time as they earn rewards. The value of xALGO increases relative to ALGO as it collects rewards, and it can be redeemed for ALGO at any time.

## Requirements

### Working Environment
- Participants must use **AlgoKit** to build the oracle smart contract.
- It is recommended to familiarise yourself with the Algorand SDKs necessary to complete the challenge.

### Development Languages
- The smart contract language used should be **Python**, specifically the **Puya library**. 
- For the off-chain code, you are free to work with your preferred language. However, we do recommend you stick to either Python or JavaScript/Typescript because there are well-supported Algorand SDKs on both.

### Functional Requirements
1. You should calculate the xALGO APR off-chain using periodic readings from https://folks-finance.github.io/folks-finance-js-sdk/functions/getConsensusState.html.
2. Other smart contracts should be able to read the xALGO APR on chain.
3. There should be at least some basic level of permissions to prevent a malicious actor from writing an incorrect APR to the oracle.
4. (Optional) Bonus points for extending the functionality and/or security of the oracle. 

### Time Allotment
- Participants have **4 days** to complete the challenge.

## Evaluation Criteria

1. **Functionality**: The xALGO APR Oracle must meet the outlined requirements.
2. **Security**: Solutions that promote oracle security are preferred.
3. **Decentralisation**: Solutions that reduce oracle centralisation risks are preferred.
4. **Code Quality**: Code readability, adherence to best practices and documentation are assessed.

