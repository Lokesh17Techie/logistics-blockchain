# 🏭 Blockchain for Supply Chain & Logistics

## 📌 Overview

This project demonstrates how **blockchain technology** can be applied in **supply chain and logistics management** to ensure transparency, traceability, and tamper-proof tracking of goods.

The system simulates the movement of goods (batches) from **manufacturers → shippers → distributors → retailers**, while validators (e.g., regulatory bodies) confirm and secure each transaction by mining blocks.

✅ Ensures authenticity and integrity of records
✅ Provides full provenance for products (farm-to-store)
✅ Prevents fraud, counterfeiting, and data tampering

---

## 🚀 Features

* **Register Product Batches** by manufacturers
* **Transfer Ownership** between supply chain participants
* **Add Quality/Compliance Events** (e.g., temperature logs, inspections)
* **Mine Blocks** by validators to secure pending transactions
* **Trace Provenance** of any product batch
* **Verify Blockchain Integrity**
* **List Participants & Validators** in the system

---

## 🛠️ Technologies Used

* **Python 3.x**
* SHA-256 cryptographic hashing
* Simple blockchain data structure (blocks, transactions, chain validation)

---

## 📂 Project Structure

```
📦 supply-chain-blockchain
 ┣ 📜 supply_chain_blockchain.py   # Main project file
 ┣ 📜 README.md                    # Project documentation
```

---

## ▶️ How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/supply-chain-blockchain.git
   cd supply-chain-blockchain
   ```

2. Run the Python script:

   ```bash
   python supply_chain_blockchain.py
   ```

3. Follow the on-screen menu to simulate:

   * Registering a batch
   * Transferring custody
   * Adding compliance logs
   * Mining blocks
   * Tracing a product

---

## 🖥️ Sample Demo Run

```
1. Register product batch (Manufacturer only)
2. Transfer batch (custody change)
3. Add quality/compliance event
4. Mine pending transactions (Validator only)
5. Trace batch (provenance & current holder)
6. Show blockchain
7. Validate blockchain
8. List participants & validators
9. Exit
```

**Example Actions:**

* Manufacturer registers apples from Nashik
* Shipper transfers apples via Ship to distributor
* Quality event added (temperature log)
* Validator mines transactions → block created
* Trace shows full product provenance

---

## 🌍 Real-World Inspiration

* **IBM Food Trust** → Used by Walmart, Nestlé, Carrefour to track food safety
* **Maersk & TradeLens** → Blockchain platform for global shipping logistics

---

## 📌 Future Improvements

* Web-based UI for easier interaction
* Integration with IoT sensors for real-time quality tracking
* Smart contracts for automatic transfers/payments
* Multi-node distributed ledger simulation

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to enhance this simulation (e.g., add more features or improve the mining logic), feel free to contribute.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify.


