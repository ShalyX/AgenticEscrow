# Agentic Escrow

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![Discord](https://dcbadge.vercel.app/api/server/8Jm4v89VAu?compact=true&style=flat)](https://discord.gg/8Jm4v89VAu)
[![Telegram](https://img.shields.io/badge/Telegram--T.svg?style=social&logo=telegram)](https://t.me/genlayer)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/yeagerai.svg?style=social&label=Follow%20%40GenLayer)](https://x.com/GenLayer)

## 👀 About
Agentic Escrow is the first decentralized freelance bounty platform where AI agents act as incorruptible judges. Built on the GenLayer network, it allows clients to post bounties with natural language requirements, freelancers to submit work, and an Intelligent Contract to evaluate the submissions using LLM consensus.

## 📦 What's included
- The `AgenticEscrow.py` intelligent contract.
- A modern Vue.js frontend to interact with the contract.
- Deployment scripts for the GenLayer network.

## 🛠️ Requirements
- Ensure you have Node.js and npm installed.
- Access to the GenLayer Bradbury Testnet (or a local GenLayer Studio).

## 🚀 Steps to run this project

### 1. Configure backend environment
   Rename the `.env.example` file to `.env`, then fill in the values for your configuration if you need to run tests locally.

### 2. Deploy the contract
   Deploy the contract from `/contracts/AgenticEscrow.py` using the GenLayer CLI or Studio:
   1. Open the GenLayer Studio interface.
   2. Paste the contents of `/contracts/AgenticEscrow.py`.
   3. Deploy the contract.
   4. Note the deployed contract address.

### 3. Setup the frontend environment
   1. Navigate to the `/app` folder.
   2. Rename `.env.example` to `.env`.
   3. Add the deployed contract address to the `/app/.env` under the variable `VITE_CONTRACT_ADDRESS`.
   4. Set the `VITE_STUDIO_URL` to `https://studio.genlayer.com/api` (or your local node).

### 4. Run the frontend Vue app
   Execute the following commands in your terminal:
   ```shell
   cd app
   npm install
   npm run dev
   ```
   The terminal will display a link to access the DApp (usually at http://localhost:5173/).

## 🤖 How the Agentic Escrow Contract Works

The Agentic Escrow contract securely holds funds and evaluates submissions using AI:

1. **Creating Bounties**: Clients post tasks describing requirements in natural language and lock native GEN tokens as a reward.
2. **Submitting Work**: Freelancers submit a URL to their completed work (e.g., a GitHub link).
3. **AI Evaluation**: The `evaluate_submission` function uses GenLayer's LLM consensus architecture. The network accesses the submitted URL, reads the freelancer's work, and compares it against the client's original natural-language requirement.
4. **Resolution**: If the AI judge approves the work, the smart contract automatically releases the locked funds to the freelancer and records the AI's reasoning.

## 💬 Community
Connect with the GenLayer community to discuss, collaborate, and share insights:
- **[Discord Channel](https://discord.gg/8Jm4v89VAu)**
- **[Telegram Group](https://t.me/genlayer)**

## 📖 Documentation
For detailed information on how to build intelligent contracts and use the GenLayerJS SDK, please refer to the [GenLayer Documentation](https://docs.genlayer.com/).

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
