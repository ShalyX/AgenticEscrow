import { createClient } from "genlayer-js";
import { simulator } from "genlayer-js/chains";

class AgenticEscrow {
  contractAddress;
  client;

  constructor(contractAddress, account = null, studioUrl = null) {
    this.contractAddress = contractAddress;

    const config = {
      chain: simulator,
      ...(account ? { account } : {}),
      ...(studioUrl ? { endpoint: studioUrl } : { endpoint: import.meta.env.VITE_STUDIO_URL || "https://studio.genlayer.com/api" }),
    };
    this.client = createClient(config);
  }

  updateAccount(account) {
    this.client = createClient({ 
      chain: simulator, 
      account,
      endpoint: import.meta.env.VITE_STUDIO_URL || "https://studio.genlayer.com/api"
    });
  }

  async getAllBounties() {
    try {
      const bounties = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_all_bounties",
        args: [],
      });
      
      // Return whole integer units
      return (bounties || []).map(b => ({
        ...b,
        reward: Number(b.reward)
      }));
    } catch (e) {
      console.error("Error loading bounties:", e);
      return [];
    }
  }

  async getSubmissions(bountyId) {
    try {
      return await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_submissions",
        args: [BigInt(bountyId)],
      });
    } catch (e) {
      console.error("Error loading submissions:", e);
      return [];
    }
  }

  async createBounty(description, amount) {
    // Drop the 18-decimal scaling so it fits inside standard DB Integers.
    const amountInWei = BigInt(Math.floor(parseFloat(amount)));
    
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "create_bounty",
      args: [description],
      value: amountInWei,
    });
    return await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
      interval: 10000,
    });
  }

  async submitWork(bountyId, urlLink) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "submit_work",
      args: [BigInt(bountyId), urlLink],
    });
    return await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
      interval: 10000,
    });
  }

  async evaluateSubmission(bountyId, urlLink) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "evaluate_submission",
      args: [BigInt(bountyId), urlLink],
    });
    return await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
      interval: 10000,
      retries: 30, // Evaluating can take time for AI consensus
    });
  }

  async cancelBounty(bountyId) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "cancel_bounty",
      args: [BigInt(bountyId)],
    });
    return await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
      interval: 10000,
    });
  }
}

export default AgenticEscrow;
