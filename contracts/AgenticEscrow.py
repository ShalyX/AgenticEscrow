# { "Depends": "py-genlayer:test" }
from genlayer import *
from dataclasses import dataclass
import json

# Status Codes
STATUS_OPEN = u256(0)
STATUS_IN_REVIEW = u256(1)
STATUS_ACCEPTED = u256(2)
STATUS_CANCELLED = u256(3)

# Rejection Categories
CAT_SUCCESS = 0
CAT_MINOR = 1
CAT_MAJOR = 2

@allow_storage
@dataclass
class Submission:
    freelancer: Address
    url: str
    evaluation: str
    category: u256  # Changed to u256 for schema consistency
    reason: str
    feedback: str
    timestamp: u256

@allow_storage
@dataclass
class Bounty:
    id: u256
    client: Address
    description: str
    reward: u256
    status: u256
    freelancer: Address
    submissions: DynArray[Submission]

class AgenticEscrow(gl.Contract):
    bounties: TreeMap[u256, Bounty]
    bounty_count: u256

    def __init__(self):
        self.bounty_count = u256(0)

    @gl.public.write.payable
    def create_bounty(self, description: str) -> u256:
        reward = gl.message.value
        assert reward > u256(0), "Bounty reward must be greater than 0"
        
        bounty_id = self.bounty_count
        self.bounty_count += u256(1)
        
        new_bounty = Bounty(
            id=bounty_id,
            client=gl.message.sender_address,
            description=description,
            reward=reward,
            status=STATUS_OPEN,
            freelancer=Address("0x0000000000000000000000000000000000000000"),
            submissions=DynArray[Submission]()
        )
        self.bounties[bounty_id] = new_bounty
        return bounty_id

    @gl.public.write
    def submit_work(self, bounty_id: u256, url_link: str):
        assert bounty_id in self.bounties, "Bounty does not exist"
        bounty = self.bounties[bounty_id]
        assert bounty.status == STATUS_OPEN or bounty.status == STATUS_IN_REVIEW, "Bounty is not active"
        
        bounty.status = STATUS_IN_REVIEW

    @gl.public.write
    def evaluate_submission(self, bounty_id: u256, url_link: str):
        self._require_bounty_active(bounty_id)
        bounty = self.bounties[bounty_id]
        
        # The AI Evaluation Logic
        eval_result = self._ai_judge(bounty.description, url_link)
        
        category = u256(int(eval_result.get("category", CAT_MAJOR)))
        reason = eval_result.get("reason", "No reason provided")
        feedback = eval_result.get("feedback", "No specific feedback provided")
        
        submission = Submission(
            freelancer=gl.message.sender_address,
            url=url_link,
            evaluation=json.dumps(eval_result),
            category=category,
            reason=reason,
            feedback=feedback,
            timestamp=u256(0) 
        )
        bounty.submissions.append(submission)
        
        if category == u256(CAT_SUCCESS):
            bounty.status = STATUS_ACCEPTED
            bounty.freelancer = gl.message.sender_address
            # Transfer reward
            self._transfer_funds(gl.message.sender_address, bounty.reward)
        elif category == u256(CAT_MAJOR):
            bounty.status = STATUS_OPEN
        else:
            # Minor bug, status stays OPEN
            bounty.status = STATUS_OPEN 

    def _ai_judge(self, requirement: str, submission_url: str) -> dict:
        def judge() -> str:
            try:
                content = gl.get_webpage(submission_url, mode="text")
            except:
                content = "Error: Could not fetch content from URL."

            task = f"""
You are an expert technical arbitrator. 
Client Requirement: {requirement}
Freelancer Submission Content: 
---
{content}
---

Evaluate if the submission meets the requirement.
Categorize the result:
0 - SUCCESS: Meets all criteria.
1 - MINOR_BUG: Almost there, but small issues found.
2 - MAJOR_FAILURE: Does not meet criteria or is irrelevant.

Respond ONLY in JSON:
{{
    "category": int,
    "reason": "Detailed explanation of why it passed or failed",
    "feedback": "Specific advice for the freelancer"
}}
"""
            result_str = gl.exec_prompt(task).replace("```json", "").replace("```", "")
            return json.dumps(json.loads(result_str), sort_keys=True)

        result_json = json.loads(gl.eq_principle_strict_eq(judge))
        return result_json

    def _require_bounty_active(self, bounty_id: u256):
        assert bounty_id in self.bounties, "Bounty does not exist"
        assert self.bounties[bounty_id].status != STATUS_ACCEPTED, "Bounty already completed"
        assert self.bounties[bounty_id].status != STATUS_CANCELLED, "Bounty cancelled"

    def _transfer_funds(self, recipient_address: Address, amount: u256):
        recipient = gl.get_contract_at(recipient_address)
        recipient.transfer(value=amount)

    @gl.public.write
    def cancel_bounty(self, bounty_id: u256):
        assert bounty_id in self.bounties, "Bounty does not exist"
        bounty = self.bounties[bounty_id]
        assert bounty.client == gl.message.sender_address, "Only client can cancel"
        assert bounty.status == STATUS_OPEN, "Cannot cancel bounty in review or completed"
        
        bounty.status = STATUS_CANCELLED
        self._transfer_funds(bounty.client, bounty.reward)

    @gl.public.view
    def get_bounty(self, bounty_id: u256) -> dict:
        b = self.bounties[bounty_id]
        return {
            "id": int(b.id),
            "client": b.client.as_hex,
            "description": b.description,
            "reward": int(b.reward),
            "status": int(b.status),
            "freelancer": b.freelancer.as_hex,
            "submissions_count": len(b.submissions)
        }

    @gl.public.view
    def get_submissions(self, bounty_id: u256) -> list:
        b = self.bounties[bounty_id]
        result = []
        for i in range(len(b.submissions)):
            s = b.submissions[i]
            result.append({
                "freelancer": s.freelancer.as_hex,
                "url": s.url,
                "category": int(s.category),
                "reason": s.reason,
                "feedback": s.feedback
            })
        return result

    @gl.public.view
    def get_all_bounties(self) -> list:
        result = []
        for i in range(int(self.bounty_count)):
            b = self.bounties[u256(i)]
            result.append({
                "id": i,
                "client": b.client.as_hex,
                "description": b.description,
                "reward": int(b.reward),
                "status": int(b.status),
                "freelancer": b.freelancer.as_hex,
                "submissions_count": len(b.submissions)
            })
        return result
