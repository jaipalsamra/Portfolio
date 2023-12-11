using System;
using System.Security.Cryptography;
using System.Text;


namespace BlockchainAssignment
{
    class Transaction
    {
        public String Hash, Signature, SenderAddress, RecipientAddress;
        public DateTime timestamp;
        public float amount, fee;


public Transaction(String SenderAddress, String sPrivKey, String RecipientAddress, float amount, float fee)
{
    this.SenderAddress = SenderAddress;
    this.RecipientAddress = RecipientAddress;
    this.amount = amount;
    this.fee = fee;
    timestamp = DateTime.Now;
    Hash = CreateHash();
    Signature = Wallet.Wallet.CreateSignature(SenderAddress, sPrivKey, Hash);
}
        public String CreateHash()
        {
            SHA256 hasher;
            hasher = SHA256Managed.Create();
            String input = SenderAddress + RecipientAddress + timestamp.ToString() + amount.ToString() + fee.ToString();
            Byte[] hashByte = hasher.ComputeHash(Encoding.UTF8.GetBytes((input)));
            String hash = string.Empty;
            foreach (byte x in hashByte)
            {
                hash += String.Format("{0:x2}", x);
            }
            return hash;
        }

        public String ReturnInfo()
        {
            return "[TRANSACTION START]" +
                "\nTransaction Hash: " + Hash +
                "\nDigital Signature: " + Signature +
                "\nTimestamp: " + timestamp +
                "\nTransferred: " + amount.ToString() + " Assignment Coin" +
                "\nFees: " + fee.ToString() +
                "\nSender Address: " + SenderAddress +
                "\nReciever Address: " + RecipientAddress +
                "\n  [TRANSACTION END]";
        }
    }
}
