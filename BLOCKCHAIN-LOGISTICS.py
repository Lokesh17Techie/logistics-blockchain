import hashlib
import time
import json


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions        # list[dict]
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Block mined: {self.hash}")


class SupplyChainBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3
        self.pending_tx = []

        # Authorized participants (ID -> Name/Role)
        self.participants = {
            "MFG001": "Acme Foods (Manufacturer)",
            "SHP001": "Oceanic Shippers (Shipper)",
            "DST001": "FreshDistrib (Distributor)",
            "RTL001": "CityMart (Retailer)"
        }

        # Validators (who are allowed to mine/validate)
        self.validators = {
            "REG001": "Food Safety Authority",
            "REG002": "Logistics Audit Node"
        }

    def create_genesis_block(self):
        return Block(0, time.time(), ["Genesis Block: Supply Chain Ledger"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    # ---------- Core actions ----------

    def register_batch(self, manufacturer_id, batch_id, product_name, quantity, origin):
        if manufacturer_id not in self.participants or "Manufacturer" not in self.participants[manufacturer_id]:
            print("⛔ Only a registered Manufacturer can register a new batch.")
            return

        # Ensure batch not already registered
        if self.current_holder(batch_id) is not None or self._batch_exists_in_pending(batch_id):
            print("⛔ Batch ID already exists. Use a unique batch id.")
            return

        self.pending_tx.append({
            "type": "REGISTER_BATCH",
            "batch_id": batch_id,
            "product": product_name,
            "qty": quantity,
            "origin": origin,
            "holder": manufacturer_id,
            "actor": manufacturer_id,
            "note": "Initial registration"
        })
        print(f"✅ Batch {batch_id} registered by {self.participants[manufacturer_id]}")

    def transfer_batch(self, from_id, to_id, batch_id, location, transport_mode="TRUCK"):
        if from_id not in self.participants or to_id not in self.participants:
            print("⛔ Unknown participant(s).")
            return

        holder = self.current_holder(batch_id)
        if holder is None:
            print("⛔ Transfer failed: unknown batch.")
            return
        if holder != from_id:
            print("⛔ Transfer failed: current holder mismatch.")
            return

        self.pending_tx.append({
            "type": "TRANSFER",
            "batch_id": batch_id,
            "from": from_id,
            "to": to_id,
            "location": location,
            "mode": transport_mode,
            "actor": from_id
        })
        print(f"🔄 Transfer queued: {batch_id} {self.participants[from_id]} ➜ {self.participants[to_id]} at {location} via {transport_mode}")

    def add_quality_event(self, actor_id, batch_id, event_type, data):
        # any known participant can log a QC/telemetry event
        if actor_id not in self.participants and actor_id not in self.validators:
            print("⛔ Unknown actor.")
            return

        if self.current_holder(batch_id) is None:
            print("⛔ Cannot log quality event: unknown batch.")
            return

        self.pending_tx.append({
            "type": "QUALITY_EVENT",
            "batch_id": batch_id,
            "event": event_type,     # e.g., "TEMP_LOG", "INSPECTION_PASSED", "RECALL_NOTICE"
            "data": data,
            "actor": actor_id
        })
        print(f"🧪 Quality event added for {batch_id}: {event_type}")

    def mine_pending(self, validator_id):
        if validator_id not in self.validators:
            print("⛔ Only validator nodes can mine/validate blocks.")
            # clear nothing; just deny
            return

        if not self.pending_tx:
            print("ℹ️ No pending transactions.")
            return

        # Apply simple sanity checks just before mining (e.g., dedupe conflicting transfers in one block)
        # For demo simplicity we skip advanced checks.

        block = Block(len(self.chain), time.time(), self.pending_tx, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        print(f"📦 Block #{block.index} validated by {self.validators[validator_id]} with {len(block.transactions)} tx(s).")
        self.pending_tx = []

    # ---------- Queries / State ----------

    def current_holder(self, batch_id):
        """Return current holder ID or None if unknown."""
        history = self._history(batch_id)
        if not history:
            # check pending REGISTER in mempool
            for tx in self.pending_tx:
                if isinstance(tx, dict) and tx.get("type") == "REGISTER_BATCH" and tx.get("batch_id") == batch_id:
                    return tx.get("holder")
            return None

        # walk through history and pending to compute holder
        holder = None
        for tx in history:
            if tx["type"] == "REGISTER_BATCH":
                holder = tx["holder"]
            elif tx["type"] == "TRANSFER":
                holder = tx["to"]

        # include pending transfers for a near-real-time view
        for tx in self.pending_tx:
            if isinstance(tx, dict) and tx.get("batch_id") == batch_id and tx.get("type") == "TRANSFER":
                holder = tx.get("to")

        return holder

    def trace(self, batch_id):
        """Print full provenance: registration, transfers, QC events."""
        events = []
        for block in self.chain:
            for tx in block.transactions:
                if isinstance(tx, dict) and tx.get("batch_id") == batch_id:
                    events.append(tx)
        for tx in self.pending_tx:
            if isinstance(tx, dict) and tx.get("batch_id") == batch_id:
                events.append({**tx, "_pending": True})

        if not events:
            print(f"⚠️ No records found for batch {batch_id}.")
            return

        print(f"\n📜 Provenance for Batch {batch_id}:")
        for e in events:
            print(json.dumps(e, indent=4))

        holder = self.current_holder(batch_id)
        if holder:
            print(f"\n🔎 Current holder: {holder} ({self.participants.get(holder, holder)})")

    def print_chain(self):
        for block in self.chain:
            print(json.dumps({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }, indent=4))
            print("-" * 60)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    # ---------- Helpers ----------

    def _history(self, batch_id):
        hist = []
        for block in self.chain:
            for tx in block.transactions:
                if isinstance(tx, dict) and tx.get("batch_id") == batch_id:
                    hist.append(tx)
        return hist

    def _batch_exists_in_pending(self, batch_id):
        return any(
            isinstance(tx, dict) and tx.get("type") == "REGISTER_BATCH" and tx.get("batch_id") == batch_id
            for tx in self.pending_tx
        )


# --- CLI Demo ---
if __name__ == "__main__":
    sc = SupplyChainBlockchain()

    while True:
        print("\n=== Blockchain Supply Chain & Logistics ===")
        print("1. Register product batch (Manufacturer only)")
        print("2. Transfer batch (custody change)")
        print("3. Add quality/compliance event")
        print("4. Mine pending transactions (Validator only)")
        print("5. Trace batch (provenance & current holder)")
        print("6. Show blockchain")
        print("7. Validate blockchain")
        print("8. List participants & validators")
        print("9. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            mfg = input("Manufacturer ID: ")           # e.g., MFG001
            bid = input("Batch ID: ")                  # e.g., BATCH-APPLE-0001
            prod = input("Product name: ")             # e.g., 'Apples'
            qty = input("Quantity: ")
            origin = input("Origin (farm/plant): ")
            sc.register_batch(mfg, bid, prod, qty, origin)

        elif choice == "2":
            frm = input("From (current holder ID): ")   # e.g., MFG001
            to = input("To (receiver ID): ")            # e.g., SHP001
            bid = input("Batch ID: ")
            loc = input("Location (city/port): ")
            mode = input("Transport mode (TRUCK/SHIP/AIR) [default TRUCK]: ") or "TRUCK"
            sc.transfer_batch(frm, to, bid, loc, mode)

        elif choice == "3":
            actor = input("Actor ID (participant/validator): ")
            bid = input("Batch ID: ")
            etype = input("Event type (TEMP_LOG/INSPECTION_PASSED/etc.): ")
            data = input("Event data (e.g., temp=4C, inspector=ID): ")
            sc.add_quality_event(actor, bid, etype, data)

        elif choice == "4":
            vid = input("Validator ID: ")              # e.g., REG001
            sc.mine_pending(vid)

        elif choice == "5":
            bid = input("Batch ID to trace: ")
            sc.trace(bid)

        elif choice == "6":
            sc.print_chain()

        elif choice == "7":
            print("Blockchain valid?", sc.is_chain_valid())

        elif choice == "8":
            print("\nParticipants:")
            for k, v in sc.participants.items():
                print(f"  {k} -> {v}")
            print("\nValidators:")
            for k, v in sc.validators.items():
                print(f"  {k} -> {v}")

        elif choice == "9":
            break

        else:
            print("Invalid choice, try again.")
